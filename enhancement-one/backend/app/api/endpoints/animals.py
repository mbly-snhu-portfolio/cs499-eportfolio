"""
Animals API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import Optional, Dict, Any
from app.models.animal import (
    AnimalCreate,
    AnimalUpdate,
    AnimalResponse,
    AnimalListResponse,
    RescueCategoryFilter
)
from app.services.animal_shelter_service import AnimalShelterService
from app.services.auth_service import get_current_active_user, get_current_admin_user
from app.services.audit_service import audit_service
from app.core.errors import AnimalNotFoundError
from app.core.rate_limit import limiter
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/animals", tags=["animals"])


def get_animal_service() -> AnimalShelterService:
    """Dependency to get animal service instance."""
    return AnimalShelterService()


@router.get("", response_model=AnimalListResponse)
@limiter.limit("60/minute")
async def list_animals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = Query(None, description="Rescue category filter"),
    animal_type: Optional[str] = Query(None),
    breed: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_active_user),
    request: Request = None,
    service: AnimalShelterService = Depends(get_animal_service)
):
    """
    List animals with pagination and filtering.
    
    Supports rescue category filtering and general filters.
    """
    try:
        # Build query criteria
        criteria: Dict[str, Any] = {}
        
        if category and category != "Reset":
            criteria = service.get_rescue_category_criteria(category)
        else:
            if animal_type:
                criteria["animal_type"] = animal_type
            if breed:
                criteria["breed"] = {"$regex": breed, "$options": "i"}
        
        # Get animals
        animals = service.read(criteria=criteria, skip=skip, limit=limit)
        total = service.count(criteria)
        
        # Audit log
        audit_service.log_operation(
            action="READ",
            collection="animals",
            user_id=current_user["id"],
            username=current_user["username"],
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        
        return AnimalListResponse(
            items=[AnimalResponse(**animal, id=animal.get("_id", "")) for animal in animals],
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        logger.error(f"Error listing animals: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{animal_id}", response_model=AnimalResponse)
async def get_animal(
    animal_id: str,
    current_user: dict = Depends(get_current_active_user),
    request: Request = None,
    service: AnimalShelterService = Depends(get_animal_service)
):
    """Get a single animal by ID."""
    try:
        animal = service.read_by_id(animal_id)
        if not animal:
            raise AnimalNotFoundError(animal_id)
        
        # Audit log
        audit_service.log_operation(
            action="READ",
            collection="animals",
            user_id=current_user["id"],
            username=current_user["username"],
            document_id=animal_id,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        
        return AnimalResponse(**animal, id=animal.get("_id", ""))
    except AnimalNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error getting animal: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=AnimalResponse, status_code=201)
async def create_animal(
    animal: AnimalCreate,
    current_user: dict = Depends(get_current_admin_user),
    request: Request = None,
    service: AnimalShelterService = Depends(get_animal_service)
):
    """Create a new animal (admin only)."""
    try:
        animal_data = animal.model_dump(exclude={"id"})
        created = service.create(animal_data)
        
        if not created:
            raise HTTPException(status_code=500, detail="Failed to create animal")
        
        # Audit log
        audit_service.log_operation(
            action="CREATE",
            collection="animals",
            user_id=current_user["id"],
            username=current_user["username"],
            document_id=created.get("_id"),
            changes={"new": animal_data},
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        
        return AnimalResponse(**created, id=created.get("_id", ""))
    except Exception as e:
        logger.error(f"Error creating animal: {str(e)}")
        audit_service.log_operation(
            action="CREATE",
            collection="animals",
            user_id=current_user["id"],
            username=current_user["username"],
            success=False,
            error_message=str(e),
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{animal_id}", response_model=AnimalResponse)
async def update_animal(
    animal_id: str,
    animal_update: AnimalUpdate,
    current_user: dict = Depends(get_current_admin_user),
    request: Request = None,
    service: AnimalShelterService = Depends(get_animal_service)
):
    """Update an animal (admin only)."""
    try:
        # Get existing animal for audit
        existing = service.read_by_id(animal_id)
        if not existing:
            raise AnimalNotFoundError(animal_id)
        
        update_data = animal_update.model_dump(exclude_unset=True)
        modified_count = service.update(animal_id, update_data)
        
        if modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to update animal")
        
        # Get updated animal
        updated = service.read_by_id(animal_id)
        
        # Audit log
        audit_service.log_operation(
            action="UPDATE",
            collection="animals",
            user_id=current_user["id"],
            username=current_user["username"],
            document_id=animal_id,
            changes={"before": existing, "after": updated},
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        
        return AnimalResponse(**updated, id=updated.get("_id", ""))
    except AnimalNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error updating animal: {str(e)}")
        audit_service.log_operation(
            action="UPDATE",
            collection="animals",
            user_id=current_user["id"],
            username=current_user["username"],
            document_id=animal_id,
            success=False,
            error_message=str(e),
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{animal_id}", status_code=204)
async def delete_animal(
    animal_id: str,
    current_user: dict = Depends(get_current_admin_user),
    request: Request = None,
    service: AnimalShelterService = Depends(get_animal_service)
):
    """Delete an animal (admin only)."""
    try:
        # Get existing animal for audit
        existing = service.read_by_id(animal_id)
        if not existing:
            raise AnimalNotFoundError(animal_id)
        
        deleted_count = service.delete(animal_id)
        
        if deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete animal")
        
        # Audit log
        audit_service.log_operation(
            action="DELETE",
            collection="animals",
            user_id=current_user["id"],
            username=current_user["username"],
            document_id=animal_id,
            changes={"deleted": existing},
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        
        return None
    except AnimalNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error deleting animal: {str(e)}")
        audit_service.log_operation(
            action="DELETE",
            collection="animals",
            user_id=current_user["id"],
            username=current_user["username"],
            document_id=animal_id,
            success=False,
            error_message=str(e),
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        raise HTTPException(status_code=500, detail=str(e))


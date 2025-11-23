"""
Analytics API endpoints.
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.services.animal_shelter_service import AnimalShelterService
from app.services.auth_service import get_current_active_user
from pymongo.collection import Collection
from app.core.database import db_manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


def get_animal_service() -> AnimalShelterService:
    """Dependency to get animal service instance."""
    return AnimalShelterService()


@router.get("/breeds")
async def get_breed_analytics(
    category: Optional[str] = Query(None, description="Rescue category filter"),
    limit: int = Query(10, ge=1, le=50),
    current_user: dict = Depends(get_current_active_user),
    service: AnimalShelterService = Depends(get_animal_service)
):
    """
    Get breed statistics and analytics.
    
    Returns top breeds by count, optionally filtered by rescue category.
    """
    try:
        collection: Collection = db_manager.get_collection()
        
        # Build match stage
        match_criteria = {}
        if category and category != "Reset":
            match_criteria = service.get_rescue_category_criteria(category)
        
        # Aggregation pipeline
        pipeline = [
            {"$match": match_criteria} if match_criteria else {"$match": {}},
            {
                "$group": {
                    "_id": "$breed",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        
        results = list(collection.aggregate(pipeline))
        
        return {
            "breeds": [
                {"breed": item["_id"], "count": item["count"]}
                for item in results
            ],
            "total_breeds": len(results)
        }
    except Exception as e:
        logger.error(f"Error getting breed analytics: {str(e)}")
        raise


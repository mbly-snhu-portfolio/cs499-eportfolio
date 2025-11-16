"""
Animal Shelter service for database operations.
"""
from typing import Dict, List, Optional, Any
import logging
from pymongo.collection import Collection
from bson.objectid import ObjectId
from app.core.database import db_manager

logger = logging.getLogger(__name__)


class AnimalShelterService:
    """Service layer for animal shelter operations."""
    
    def __init__(self):
        """Initialize the service with database collection."""
        self.collection = db_manager.get_collection()
        self.database = db_manager.get_database()
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new animal record.
        
        Args:
            data: Animal data dictionary
            
        Returns:
            Created animal document
        """
        try:
            if not data:
                raise ValueError("Data cannot be empty")
            
            result = self.collection.insert_one(data)
            if result.inserted_id:
                created = self.collection.find_one(
                    {"_id": result.inserted_id}
                )
                if created:
                    created["_id"] = str(created["_id"])
                return created
            raise Exception("Failed to create animal")
        except Exception as e:
            logger.error(f"Error creating animal: {str(e)}")
            raise
    
    def read(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[tuple]] = None
    ) -> List[Dict[str, Any]]:
        """
        Read animal records with pagination.
        
        Args:
            criteria: Query criteria
            skip: Number of records to skip
            limit: Maximum number of records to return
            sort: Sort specification
            
        Returns:
            List of animal documents
        """
        try:
            criteria = criteria or {}
            cursor = self.collection.find(criteria)
            
            if sort:
                cursor = cursor.sort(sort)
            
            cursor = cursor.skip(skip).limit(limit)
            
            results = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                results.append(doc)
            
            return results
        except Exception as e:
            logger.error(f"Error reading animals: {str(e)}")
            raise
    
    def read_by_id(self, animal_id: str) -> Optional[Dict[str, Any]]:
        """
        Read a single animal by ID.
        
        Args:
            animal_id: Animal ID or MongoDB ObjectId
            
        Returns:
            Animal document or None
        """
        try:
            # Try ObjectId first
            try:
                query = {"_id": ObjectId(animal_id)}
            except Exception:
                query = {"animal_id": animal_id}
            
            doc = self.shelter.collection.find_one(query)
            if doc:
                doc["_id"] = str(doc["_id"])
            return doc
        except Exception as e:
            logger.error(f"Error reading animal by ID: {str(e)}")
            raise
    
    def update(
        self,
        animal_id: str,
        update_data: Dict[str, Any]
    ) -> int:
        """
        Update an animal record.
        
        Args:
            animal_id: Animal ID or MongoDB ObjectId
            update_data: Fields to update
            
        Returns:
            Number of modified documents
        """
        try:
            # Try ObjectId first
            try:
                criteria = {"_id": ObjectId(animal_id)}
            except Exception:
                criteria = {"animal_id": animal_id}
            
            result = self.collection.update_many(
                criteria,
                {"$set": update_data}
            )
            return result.modified_count
        except Exception as e:
            logger.error(f"Error updating animal: {str(e)}")
            raise
    
    def delete(self, animal_id: str) -> int:
        """
        Delete an animal record.
        
        Args:
            animal_id: Animal ID or MongoDB ObjectId
            
        Returns:
            Number of deleted documents
        """
        try:
            # Try ObjectId first
            try:
                criteria = {"_id": ObjectId(animal_id)}
            except Exception:
                criteria = {"animal_id": animal_id}
            
            result = self.collection.delete_many(criteria)
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting animal: {str(e)}")
            raise
    
    def count(self, criteria: Optional[Dict[str, Any]] = None) -> int:
        """
        Count animals matching criteria.
        
        Args:
            criteria: Query criteria
            
        Returns:
            Count of matching documents
        """
        try:
            criteria = criteria or {}
            return self.collection.count_documents(criteria)
        except Exception as e:
            logger.error(f"Error counting animals: {str(e)}")
            raise
    
    def get_rescue_category_criteria(self, category: str) -> Dict[str, Any]:
        """
        Get MongoDB query criteria for rescue category.
        
        Args:
            category: Rescue category name
            
        Returns:
            MongoDB query criteria
        """
        if category == "Water Rescue":
            return {
                "$and": [
                    {"animal_type": "Dog"},
                    {"breed": {"$regex": "Labrador|Chesapeake Bay Retriever|Newfoundland", "$options": "i"}},
                    {"sex_upon_outcome": {"$regex": "Intact", "$options": "i"}}
                ]
            }
        elif category == "Mountain or Wilderness Rescue":
            return {
                "$and": [
                    {"animal_type": "Dog"},
                    {"breed": {"$regex": "German Shepherd|Alaskan Malamute|Old English Sheepdog|Rottweiler|Saint Bernard", "$options": "i"}},
                    {"sex_upon_outcome": {"$regex": "Intact", "$options": "i"}}
                ]
            }
        elif category == "Disaster or Individual Tracking":
            return {
                "$and": [
                    {"animal_type": "Dog"},
                    {"breed": {"$regex": "German Shepherd|Bloodhound|Belgian Malinois", "$options": "i"}},
                    {"sex_upon_outcome": {"$regex": "Intact", "$options": "i"}}
                ]
            }
        else:
            return {}


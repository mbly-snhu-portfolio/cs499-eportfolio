"""
Animal Shelter service for database operations.
"""
from typing import Dict, List, Optional, Any, Set
import logging
from pymongo.collection import Collection
from bson.objectid import ObjectId
from app.core.database import db_manager
from app.utils.trie import Trie
from app.utils.cache import get_from_cache, set_in_cache, delete_from_cache, _generate_cache_key, invalidate_pattern
from app.utils.fuzzy_match import fuzzy_search, find_best_matches
from app.core.config import settings

logger = logging.getLogger(__name__)


class AnimalShelterService:
    """Service layer for animal shelter operations."""
    
    def __init__(self):
        """Initialize the service with database collection."""
        self.collection = db_manager.get_collection()
        self.database = db_manager.get_database()
        self._breed_trie: Optional[Trie] = None
        self._name_trie: Optional[Trie] = None
        self._trie_initialized = False
    
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
            
            doc = self.collection.find_one(query)
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
    
    def _initialize_tries(self) -> None:
        """Initialize Trie data structures for breeds and names."""
        if self._trie_initialized:
            return
        
        try:
            # Check cache first
            cache_key = "trie:breeds"
            cached_breeds = get_from_cache(cache_key)
            
            if cached_breeds is None:
                # Build breed Trie from database
                breeds = self.collection.distinct("breed")
                breeds = [b for b in breeds if b]  # Filter None values
                set_in_cache(cache_key, breeds, ttl=86400)  # Cache for 24 hours
            else:
                breeds = cached_breeds
            
            self._breed_trie = Trie()
            self._breed_trie.build_from_list(breeds)
            
            # Build name Trie (using name field if available)
            cache_key = "trie:names"
            cached_names = get_from_cache(cache_key)
            
            if cached_names is None:
                names = self.collection.distinct("name")
                names = [n for n in names if n]  # Filter None values
                set_in_cache(cache_key, names, ttl=86400)
            else:
                names = cached_names
            
            self._name_trie = Trie()
            self._name_trie.build_from_list(names)
            
            self._trie_initialized = True
            logger.info("Trie data structures initialized")
        except Exception as e:
            logger.error(f"Error initializing tries: {str(e)}")
            # Create empty tries as fallback
            self._breed_trie = Trie()
            self._name_trie = Trie()
    
    def autocomplete_breeds(self, prefix: str, limit: int = 10) -> List[str]:
        """
        Get breed autocomplete suggestions using Trie.
        
        Args:
            prefix: Prefix to search for
            limit: Maximum number of results
            
        Returns:
            List of breed suggestions
        """
        self._initialize_tries()
        if not self._breed_trie:
            return []
        return self._breed_trie.search_prefix(prefix, limit)
    
    def autocomplete_names(self, prefix: str, limit: int = 10) -> List[str]:
        """
        Get name autocomplete suggestions using Trie.
        
        Args:
            prefix: Prefix to search for
            limit: Maximum number of results
            
        Returns:
            List of name suggestions
        """
        self._initialize_tries()
        if not self._name_trie:
            return []
        return self._name_trie.search_prefix(prefix, limit)
    
    def fuzzy_search_breeds(self, query: str, threshold: float = 0.6, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Perform fuzzy search on breeds using Levenshtein distance.
        
        Args:
            query: Search query
            threshold: Similarity threshold (0.0 to 1.0)
            limit: Maximum number of results
            
        Returns:
            List of animals with matching breeds
        """
        try:
            # Get all distinct breeds
            breeds = self.collection.distinct("breed")
            breeds = [b for b in breeds if b]
            
            # Find best matching breeds
            matches = find_best_matches(query, breeds, threshold, limit)
            
            if not matches:
                return []
            
            # Query animals with matching breeds
            breed_list = [breed for breed, _ in matches]
            criteria = {"breed": {"$in": breed_list}}
            
            animals = self.read(criteria=criteria, limit=limit * 2)  # Get more to allow for ranking
            
            # Sort by breed similarity
            breed_similarity = {breed: sim for breed, sim in matches}
            animals.sort(key=lambda a: breed_similarity.get(a.get("breed", ""), 0), reverse=True)
            
            return animals[:limit]
        except Exception as e:
            logger.error(f"Error in fuzzy breed search: {str(e)}")
            return []
    
    def read_cached(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[tuple]] = None
    ) -> List[Dict[str, Any]]:
        """
        Read animal records with caching.
        
        Args:
            criteria: Query criteria
            skip: Number of records to skip
            limit: Maximum number of records to return
            sort: Sort specification
            
        Returns:
            List of animal documents
        """
        # Generate cache key
        cache_key = _generate_cache_key("animals:read", criteria, skip, limit, sort)
        
        # Try cache first
        cached_result = get_from_cache(cache_key)
        if cached_result is not None:
            logger.debug(f"Cache hit for key: {cache_key}")
            return cached_result
        
        # Cache miss, query database
        result = self.read(criteria, skip, limit, sort)
        
        # Store in cache
        set_in_cache(cache_key, result, ttl=settings.cache_ttl_seconds)
        logger.debug(f"Cache miss, stored result for key: {cache_key}")
        
        return result
    
    def invalidate_cache(self) -> None:
        """Invalidate all animal-related cache entries."""
        try:
            # Invalidate common patterns
            patterns = ["animals:*", "trie:*"]
            for pattern in patterns:
                count = invalidate_pattern(pattern)
                if count > 0:
                    logger.info(f"Invalidated {count} cache entries matching {pattern}")
        except Exception as e:
            logger.error(f"Error invalidating cache: {str(e)}")


"""Animal shelter service facade.

This module intentionally stays small (~200 LOC) and delegates to the
pluggable animal-domain services under `app.services.animals`.
"""

from typing import Any, Dict, List, Optional

from app.services.animals.repository import get_animal_repository
from app.services.animals.criteria import get_rescue_category_criteria
from app.services.animals.crud import AnimalCrud
from app.services.animals.cache_ops import AnimalCacheOps
from app.services.animals.search import AnimalSearchService
from app.services.animals.analytics import AnimalAnalyticsService


class AnimalShelterService:
    """Public service API used by endpoints and verification scripts."""

    def __init__(self):
        repo = get_animal_repository()

        self.collection = repo.collection
        self.database = repo.database

        self._crud = AnimalCrud(self.collection)
        self._cache = AnimalCacheOps(self._crud)
        self._search = AnimalSearchService(self.collection)
        self._analytics = AnimalAnalyticsService(self.collection)

    # CRUD
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._crud.create(data)

    def read(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[tuple]] = None,
    ) -> List[Dict[str, Any]]:
        return self._crud.read(criteria=criteria, skip=skip, limit=limit, sort=sort)

    def read_by_id(self, animal_id: str) -> Optional[Dict[str, Any]]:
        return self._crud.read_by_id(animal_id)

    def update(self, animal_id: str, update_data: Dict[str, Any]) -> int:
        return self._crud.update(animal_id, update_data)

    def delete(self, animal_id: str) -> int:
        return self._crud.delete(animal_id)

    def count(self, criteria: Optional[Dict[str, Any]] = None) -> int:
        return self._crud.count(criteria)

    # Filtering
    def get_rescue_category_criteria(self, category: str) -> Dict[str, Any]:
        return get_rescue_category_criteria(category)

    # Search and algorithms
    def autocomplete_breeds(self, prefix: str, limit: int = 10) -> List[str]:
        return self._search.autocomplete_breeds(prefix, limit)

    def autocomplete_names(self, prefix: str, limit: int = 10) -> List[str]:
        return self._search.autocomplete_names(prefix, limit)

    # Backwards-compatible: used by tests to pre-warm tries
    def _initialize_tries(self) -> None:
        self._search._initialize_tries()

    def fuzzy_search_breeds(
        self, query: str, threshold: float = 0.6, limit: int = 10
    ) -> List[Dict[str, Any]]:
        return self._search.fuzzy_search_breeds(query, threshold, limit)

    # Caching
    def read_cached(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[tuple]] = None,
    ) -> List[Dict[str, Any]]:
        return self._cache.read_cached(criteria=criteria, skip=skip, limit=limit, sort=sort)

    def invalidate_cache(self) -> None:
        self._cache.invalidate_cache()

    # Database analytics
    def get_species_stats(self) -> List[Dict[str, Any]]:
        return self._analytics.get_species_stats()

    def ensure_indexes(self) -> None:
        self._analytics.ensure_indexes()

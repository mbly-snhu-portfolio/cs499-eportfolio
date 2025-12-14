"""Search-related services for animals (autocomplete + fuzzy search)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import logging

from app.utils.trie import Trie
from app.utils.cache import get_from_cache, set_in_cache
from app.utils.fuzzy_match import find_best_matches

logger = logging.getLogger(__name__)


class AnimalSearchService:
    """Provides trie-backed autocomplete and fuzzy breed search."""

    def __init__(self, collection):
        self.collection = collection
        self._breed_trie: Optional[Trie] = None
        self._name_trie: Optional[Trie] = None
        self._trie_initialized = False

    def _initialize_tries(self) -> None:
        if self._trie_initialized:
            return

        try:
            # Breeds
            cache_key = "trie:breeds"
            cached_breeds = get_from_cache(cache_key)
            if cached_breeds is None:
                breeds = [b for b in (self.collection.distinct("breed") or []) if b]
                set_in_cache(cache_key, breeds, ttl=86400)
            else:
                breeds = cached_breeds

            self._breed_trie = Trie()
            self._breed_trie.build_from_list(breeds)

            # Names
            cache_key = "trie:names"
            cached_names = get_from_cache(cache_key)
            if cached_names is None:
                names = [n for n in (self.collection.distinct("name") or []) if n]
                set_in_cache(cache_key, names, ttl=86400)
            else:
                names = cached_names

            self._name_trie = Trie()
            self._name_trie.build_from_list(names)

            self._trie_initialized = True
            logger.info("Trie data structures initialized")
        except Exception as e:
            logger.error(f"Error initializing tries: {str(e)}")
            self._breed_trie = Trie()
            self._name_trie = Trie()

    def autocomplete_breeds(self, prefix: str, limit: int = 10) -> List[str]:
        self._initialize_tries()
        return self._breed_trie.search_prefix(prefix, limit) if self._breed_trie else []

    def autocomplete_names(self, prefix: str, limit: int = 10) -> List[str]:
        self._initialize_tries()
        return self._name_trie.search_prefix(prefix, limit) if self._name_trie else []

    def fuzzy_search_breeds(
        self, query: str, threshold: float = 0.6, limit: int = 10
    ) -> List[Dict[str, Any]]:
        try:
            breeds = [b for b in (self.collection.distinct("breed") or []) if b]
            matches = find_best_matches(query, breeds, threshold, limit)
            if not matches:
                return []

            breed_list = [breed for breed, _ in matches]
            animals = list(self.collection.find({"breed": {"$in": breed_list}}).limit(limit * 2))

            breed_similarity = {breed: sim for breed, sim in matches}
            animals.sort(key=lambda a: breed_similarity.get(a.get("breed", ""), 0), reverse=True)

            results: List[Dict[str, Any]] = []
            for doc in animals[:limit]:
                doc["_id"] = str(doc["_id"])
                results.append(doc)
            return results
        except Exception as e:
            logger.error(f"Error in fuzzy breed search: {str(e)}")
            return []

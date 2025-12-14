"""Analytics and index management for animals."""

from __future__ import annotations

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class AnimalAnalyticsService:
    """Aggregation pipelines and index management for the animals collection."""

    def __init__(self, collection):
        self.collection = collection

    def get_species_stats(self) -> List[Dict]:
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": {"species": "$animal_type", "outcome": "$outcome_type"},
                        "count": {"$sum": 1},
                        "avg_age_weeks": {
                            "$avg": {
                                "$convert": {
                                    "input": "$age_upon_outcome_in_weeks",
                                    "to": "double",
                                    "onError": 0,
                                    "onNull": 0,
                                }
                            }
                        },
                    }
                },
                {"$sort": {"count": -1}},
                {
                    "$project": {
                        "_id": 0,
                        "species": "$_id.species",
                        "outcome": "$_id.outcome",
                        "count": 1,
                        "avg_age_weeks": {"$round": ["$avg_age_weeks", 1]},
                    }
                },
            ]
            return list(self.collection.aggregate(pipeline))
        except Exception as e:
            logger.error(f"Error getting species stats: {str(e)}")
            return []

    def ensure_indexes(self) -> None:
        try:
            self.collection.create_index(
                [("animal_type", 1), ("breed", 1)], name="idx_type_breed"
            )
            self.collection.create_index(
                [("outcome_type", 1), ("animal_type", 1)], name="idx_outcome_type"
            )
            self.collection.create_index(
                [("animal_type", 1), ("age_upon_outcome_in_weeks", 1)],
                name="idx_type_age",
            )
            self.collection.create_index(
                [("breed", "text"), ("color", "text")], name="idx_text_search"
            )
            logger.info("Advanced indexes ensured successfully")
        except Exception as e:
            logger.error(f"Error ensuring indexes: {str(e)}")

"""Query criteria builders for animals."""

from typing import Any, Dict


def get_rescue_category_criteria(category: str) -> Dict[str, Any]:
    """Get MongoDB query criteria for a rescue category."""
    if category == "Water Rescue":
        return {
            "$and": [
                {"animal_type": "Dog"},
                {
                    "breed": {
                        "$regex": "Labrador|Chesapeake Bay Retriever|Newfoundland",
                        "$options": "i",
                    }
                },
                {"sex_upon_outcome": {"$regex": "Intact", "$options": "i"}},
            ]
        }

    if category == "Mountain or Wilderness Rescue":
        return {
            "$and": [
                {"animal_type": "Dog"},
                {
                    "breed": {
                        "$regex": "German Shepherd|Alaskan Malamute|Old English Sheepdog|Rottweiler|Saint Bernard",
                        "$options": "i",
                    }
                },
                {"sex_upon_outcome": {"$regex": "Intact", "$options": "i"}},
            ]
        }

    if category == "Disaster or Individual Tracking":
        return {
            "$and": [
                {"animal_type": "Dog"},
                {
                    "breed": {
                        "$regex": "German Shepherd|Bloodhound|Belgian Malinois",
                        "$options": "i",
                    }
                },
                {"sex_upon_outcome": {"$regex": "Intact", "$options": "i"}},
            ]
        }

    return {}

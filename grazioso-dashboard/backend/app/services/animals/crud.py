"""CRUD operations for animals."""

from __future__ import annotations

from bson.objectid import ObjectId
from typing import Any, Dict, List, Optional

from app.services.audit_service import audit_service


def _id_query(animal_id: str) -> Dict[str, Any]:
    try:
        return {"_id": ObjectId(animal_id)}
    except Exception:
        return {"animal_id": animal_id}


class AnimalCrud:
    """CRUD operations for the animals collection."""

    def __init__(self, collection):
        self.collection = collection

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data:
            raise ValueError("Data cannot be empty")

        result = self.collection.insert_one(data)
        if not result.inserted_id:
            raise RuntimeError("Failed to create animal")

        created = self.collection.find_one({"_id": result.inserted_id})
        if created:
            created["_id"] = str(created["_id"])

        audit_service.log_operation(
            action="CREATE",
            collection="animals",
            user_id="system",
            username="system_user",
            document_id=str(result.inserted_id),
            changes=data,
        )

        return created

    def read(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[tuple]] = None,
    ) -> List[Dict[str, Any]]:
        criteria = criteria or {}
        cursor = self.collection.find(criteria)
        if sort:
            cursor = cursor.sort(sort)
        cursor = cursor.skip(skip).limit(limit)

        results: List[Dict[str, Any]] = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    def read_by_id(self, animal_id: str) -> Optional[Dict[str, Any]]:
        doc = self.collection.find_one(_id_query(animal_id))
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def update(self, animal_id: str, update_data: Dict[str, Any]) -> int:
        result = self.collection.update_many(_id_query(animal_id), {"$set": update_data})
        if result.modified_count > 0:
            audit_service.log_operation(
                action="UPDATE",
                collection="animals",
                user_id="system",
                username="system_user",
                document_id=animal_id,
                changes=update_data,
            )
        return result.modified_count

    def delete(self, animal_id: str) -> int:
        result = self.collection.delete_many(_id_query(animal_id))
        if result.deleted_count > 0:
            audit_service.log_operation(
                action="DELETE",
                collection="animals",
                user_id="system",
                username="system_user",
                document_id=animal_id,
            )
        return result.deleted_count

    def count(self, criteria: Optional[Dict[str, Any]] = None) -> int:
        return self.collection.count_documents(criteria or {})

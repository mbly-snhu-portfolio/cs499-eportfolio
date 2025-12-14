"""Repository helpers for the animals domain."""

from dataclasses import dataclass
from pymongo.collection import Collection
from pymongo.database import Database

from app.core.database import db_manager


@dataclass(frozen=True)
class AnimalRepository:
    """Provides access to the animals collection and its database."""

    collection: Collection
    database: Database


def get_animal_repository() -> AnimalRepository:
    """Create a repository from the global DatabaseManager."""
    return AnimalRepository(
        collection=db_manager.get_collection(),
        database=db_manager.get_database(),
    )

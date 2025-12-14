"""
Database connection and configuration.
"""
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages MongoDB connection and provides database/collection access."""
    
    def __init__(self):
        """Initialize database connection."""
        self.client: Optional[MongoClient] = None
        self.database: Optional[Database] = None
        self.collection: Optional[Collection] = None
        
    def connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
            connection_string = (
                f"mongodb://{settings.mongo_user}:{settings.mongo_pass}"
                f"@{settings.mongodb_host}:{settings.mongodb_port}"
            )
            self.client = MongoClient(connection_string)
            
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB at {settings.mongodb_host}:{settings.mongodb_port}")
            
            # Set up database and collection references
            self.database = self.client[settings.aac_database]
            self.collection = self.database[settings.aac_collection]
            
            # Verify collection exists
            if settings.aac_collection not in self.database.list_collection_names():
                logger.warning(
                    f"Collection '{settings.aac_collection}' does not exist. "
                    "It will be created on first insert."
                )
                
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise ConnectionError(f"Unable to connect to MongoDB") from e
    
    def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    def get_collection(self) -> Collection:
        """Get the animals collection."""
        if self.collection is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.collection
    
    def get_database(self) -> Database:
        """Get the database instance."""
        if self.database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.database


# Global database manager instance
db_manager = DatabaseManager()


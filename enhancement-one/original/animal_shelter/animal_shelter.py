"""
AnimalShelter CRUD Operations Module
CS 340 Module Four Milestone

This module implements CRUD (Create, Read, Update, Delete) operations for the
Austin Animal Center (AAC) animals collection using PyMongo.

Requirements following EARS format:
- The AnimalShelter class shall provide CRUD operations for the animals collection
- When create() is called with valid data, the AnimalShelter shall insert the document and return True
- When create() is called with invalid data, the AnimalShelter shall raise an exception
- When read() is called with valid criteria, the AnimalShelter shall return matching documents as a list
- When read() is called with no criteria, the AnimalShelter shall return all documents as a list
- When update() is called with valid criteria and update spec, the AnimalShelter shall return the number of modified documents
- When delete() is called with valid criteria, the AnimalShelter shall return the number of deleted documents
- The AnimalShelter class shall provide a helper to ensure indexes on common query fields
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Dict, List, Optional, Any, Union
import logging
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AnimalShelter(object):
    """
    CRUD operations for Animal collection in MongoDB

    This class provides a clean interface for performing Create and Read operations
    on the Austin Animal Center animals collection. The class follows industry
    standard best practices including proper exception handling, logging, and
    type hints for better code maintainability and reliability.
    """

    def __init__(self, user: str = None, password: str = None, host: str = None, port: int = None):
        """
        Initialize the AnimalShelter with MongoDB connection.

        Args:
            user (str): Username for authentication (default: from environment).
            password (str): Password for authentication (default: from environment).
            host (str): MongoDB host address (default: from environment).
            port (int): MongoDB port number (default: from environment).

        Raises:
            ConnectionError: If unable to connect to MongoDB
        """
        # Connection Variables - using environment variables with fallbacks
        # User/password arguments take precedence over environment variables.
        self.USER = user or os.getenv('MONGO_USER') or os.getenv('AAC_USER', 'aacuser')
        self.PASS = password or os.getenv('MONGO_PASS') or os.getenv('AAC_PASS', 'SECRET')
        self.HOST = host or os.getenv('MONGO_HOST') or os.getenv('MONGODB_HOST', 'localhost')
        self.PORT = int(port or os.getenv('MONGO_PORT') or os.getenv('MONGODB_PORT', '27017'))
        self.DB = os.getenv('AAC_DATABASE', 'aac')
        self.COL = os.getenv('AAC_COLLECTION', 'animals')

        # Initialize logging for debugging and monitoring
        self._setup_logging()

        try:
            # Initialize Connection using connection string format from rubric
            connection_string = f'mongodb://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}'
            self.client = MongoClient(connection_string)

            # Test connection
            self.client.admin.command('ping')
            self.logger.info(f"Successfully connected to MongoDB at {self.HOST}:{self.PORT}")

            # Set up database and collection references
            self.database = self.client[self.DB]
            self.collection = self.database[self.COL]

            # Verify collection exists
            if self.COL not in self.database.list_collection_names():
                self.logger.warning(f"Collection '{self.COL}' does not exist. It will be created on first insert.")

        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise ConnectionError(f"Unable to connect to MongoDB at {self.HOST}:{self.PORT}") from e

    def _setup_logging(self) -> None:
        """Configure logging for the AnimalShelter class."""
        self.logger = logging.getLogger(__name__)
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))

        # Create console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def create(self, data: Dict[str, Any]) -> bool:
        """
        Create method to implement the C in CRUD.

        When create() is called with valid data, the AnimalShelter shall insert
        the document and return True. When create() is called with invalid data,
        the AnimalShelter shall raise an exception.

        Args:
            data (Dict[str, Any]): Document data to insert into the collection.
                                  Must be a dictionary with key/value pairs.

        Returns:
            bool: True if successful insert, False otherwise

        Raises:
            ValueError: If data is None or empty
            Exception: If insertion fails due to database errors

        Example:
            >>> shelter = AnimalShelter()
            >>> animal_data = {
            ...     "animal_id": "A123456",
            ...     "name": "Buddy",
            ...     "animal_type": "Dog",
            ...     "breed": "Golden Retriever"
            ... }
            >>> result = shelter.create(animal_data)
            >>> print(result)
            True
        """
        try:
            # Validate input data
            if data is None:
                raise ValueError("Data parameter cannot be None")

            if not isinstance(data, dict):
                raise ValueError("Data parameter must be a dictionary")

            if not data:
                raise ValueError("Data parameter cannot be empty")

            # Log the insertion attempt
            self.logger.info(f"Attempting to insert document: {list(data.keys())}")

            # Insert the document into the collection
            result = self.collection.insert_one(data)

            # Verify insertion was successful
            if result.inserted_id:
                self.logger.info(f"Successfully inserted document with ID: {result.inserted_id}")
                return True
            else:
                self.logger.error("Insert operation completed but no document ID returned")
                return False

        except ValueError as ve:
            self.logger.error(f"Validation error in create method: {str(ve)}")
            raise
        except Exception as e:
            self.logger.error(f"Database error in create method: {str(e)}")
            raise Exception(f"Failed to insert document: {str(e)}") from e

    def read(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Read method to implement the R in CRUD.

        When read() is called with valid criteria, the AnimalShelter shall return
        matching documents as a list. When read() is called with no criteria,
        the AnimalShelter shall return all documents as a list.

        Args:
            criteria (Optional[Dict[str, Any]]): Query criteria to filter documents.
                                               If None, returns all documents.
                                               Must be a dictionary with key/value pairs.

        Returns:
            List[Dict[str, Any]]: List of matching documents. Empty list if no matches found.

        Raises:
            ValueError: If criteria is not a dictionary when provided
            Exception: If query fails due to database errors

        Example:
            >>> shelter = AnimalShelter()
            >>> # Find all dogs
            >>> dogs = shelter.read({"animal_type": "Dog"})
            >>> print(f"Found {len(dogs)} dogs")
            >>> # Find all animals
            >>> all_animals = shelter.read()
            >>> print(f"Total animals: {len(all_animals)}")
        """
        try:
            # Validate criteria parameter
            if criteria is not None and not isinstance(criteria, dict):
                raise ValueError("Criteria parameter must be a dictionary or None")

            # Prepare query criteria
            query = criteria if criteria is not None else {}

            # Log the query attempt
            if criteria:
                self.logger.info(f"Querying documents with criteria: {criteria}")
            else:
                self.logger.info("Querying all documents")

            # Execute the query using find() as specified in rubric
            cursor = self.collection.find(query)

            # Convert cursor to list of documents
            documents = list(cursor)

            self.logger.info(f"Query returned {len(documents)} documents")
            return documents

        except ValueError as ve:
            self.logger.error(f"Validation error in read method: {str(ve)}")
            raise
        except Exception as e:
            self.logger.error(f"Database error in read method: {str(e)}")
            raise Exception(f"Failed to query documents: {str(e)}") from e

    def read_by_id(self, animal_id: str) -> Optional[Dict[str, Any]]:
        """
        Read a single document by animal_id.

        This is a convenience method that uses the read() method internally
        but returns a single document instead of a list.

        Args:
            animal_id (str): The animal_id to search for

        Returns:
            Optional[Dict[str, Any]]: The matching document or None if not found

        Example:
            >>> shelter = AnimalShelter()
            >>> animal = shelter.read_by_id("A123456")
            >>> if animal:
            ...     print(f"Found animal: {animal['name']}")
        """
        try:
            documents = self.read({"animal_id": animal_id})
            return documents[0] if documents else None
        except Exception as e:
            self.logger.error(f"Error in read_by_id method: {str(e)}")
            raise

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the animals collection.

        Returns:
            Dict[str, Any]: Collection statistics including document count
        """
        try:
            stats = {
                "total_documents": self.collection.count_documents({}),
                "database": self.DB,
                "collection": self.COL,
                "connection_host": self.HOST,
                "connection_port": self.PORT
            }
            return stats
        except Exception as e:
            self.logger.error(f"Error getting collection stats: {str(e)}")
            raise

    def close_connection(self) -> None:
        """
        Close the MongoDB connection.

        This method should be called when the AnimalShelter object is no longer needed
        to properly clean up database connections.
        """
        try:
            if hasattr(self, 'client'):
                self.client.close()
                self.logger.info("MongoDB connection closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing MongoDB connection: {str(e)}")

    def update(self, criteria: Dict[str, Any], update_values: Dict[str, Any], many: bool = False) -> int:
        """
        Update method to implement the U in CRUD.

        Args:
            criteria (Dict[str, Any]): Query filter for documents to update.
            update_values (Dict[str, Any]): MongoDB update spec (e.g., {"$set": {...}}).
            many (bool): If True, update many documents; otherwise update one.

        Returns:
            int: Number of documents modified.

        Raises:
            ValueError: If inputs are invalid.
            Exception: If the database update fails.
        """
        try:
            if criteria is None or not isinstance(criteria, dict):
                raise ValueError("Criteria parameter must be a non-empty dictionary")
            if not isinstance(update_values, dict) or not update_values:
                raise ValueError("update_values must be a non-empty dictionary containing MongoDB update operators (e.g., $set)")
            if not any(str(k).startswith("$") for k in update_values.keys()):
                raise ValueError("update_values must contain at least one MongoDB update operator (e.g., $set, $unset, $inc)")

            self.logger.info(f"Updating documents with criteria: {criteria} using operators: {list(update_values.keys())} (many={many})")

            if many:
                result = self.collection.update_many(criteria, update_values)
            else:
                result = self.collection.update_one(criteria, update_values)

            modified = int(result.modified_count or 0)
            self.logger.info(f"Update modified_count: {modified}")
            return modified

        except ValueError:
            raise
        except Exception as e:
            self.logger.error(f"Database error in update method: {str(e)}")
            raise Exception(f"Failed to update documents: {str(e)}") from e

    def delete(self, criteria: Dict[str, Any], many: bool = False) -> int:
        """
        Delete method to implement the D in CRUD.

        Args:
            criteria (Dict[str, Any]): Query filter for documents to delete.
            many (bool): If True, delete many documents; otherwise delete one.

        Returns:
            int: Number of documents deleted.

        Raises:
            ValueError: If inputs are invalid.
            Exception: If the database delete fails.
        """
        try:
            if criteria is None or not isinstance(criteria, dict):
                raise ValueError("Criteria parameter must be a non-empty dictionary")

            self.logger.info(f"Deleting documents with criteria: {criteria} (many={many})")

            if many:
                result = self.collection.delete_many(criteria)
            else:
                result = self.collection.delete_one(criteria)

            deleted = int(result.deleted_count or 0)
            self.logger.info(f"Delete deleted_count: {deleted}")
            return deleted

        except ValueError:
            raise
        except Exception as e:
            self.logger.error(f"Database error in delete method: {str(e)}")
            raise Exception(f"Failed to delete documents: {str(e)}") from e

    def ensure_indexes(self) -> None:
        """
        Create recommended indexes to optimize common queries.
        Safe to call multiple times.
        """
        try:
            self.logger.info("Ensuring indexes on common query fields...")
            # Not enforcing unique to avoid conflicts with existing datasets unless guaranteed unique
            self.collection.create_index([("animal_id", 1)], name="idx_animal_id")
            self.collection.create_index([("animal_type", 1)], name="idx_animal_type")
            self.collection.create_index([("breed", 1)], name="idx_breed")
            self.collection.create_index([("outcome_type", 1)], name="idx_outcome_type")
            self.collection.create_index([("age_upon_outcome", 1)], name="idx_age_upon_outcome")
            self.logger.info("Indexes ensured successfully.")
        except Exception as e:
            # Index creation failures should not crash the app; log as warning
            self.logger.warning(f"Failed to create indexes: {e}")

    def __enter__(self):
        """Context manager entry point."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        self.close_connection()


# Example usage and testing
if __name__ == "__main__":
    # Example of how to use the AnimalShelter class
    try:
        # Create an instance of AnimalShelter
        shelter = AnimalShelter()

        # Example create operation
        test_animal = {
            "animal_id": "TEST001",
            "name": "Test Animal",
            "animal_type": "Dog",
            "breed": "Test Breed",
            "age_upon_outcome": "2 years",
            "outcome_type": "Adoption"
        }

        # Test create method
        create_result = shelter.create(test_animal)
        print(f"Create operation result: {create_result}")

        # Test read method
        all_animals = shelter.read()
        print(f"Total animals in collection: {len(all_animals)}")

        # Test read with criteria
        dogs = shelter.read({"animal_type": "Dog"})
        print(f"Number of dogs: {len(dogs)}")

        # Get collection statistics
        stats = shelter.get_collection_stats()
        print(f"Collection stats: {stats}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up connection
        if 'shelter' in locals():
            shelter.close_connection()

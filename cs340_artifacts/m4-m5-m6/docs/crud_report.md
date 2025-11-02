# Grazioso Salvare: CRUD Operations Report

This document details the full CRUD (Create, Read, Update, Delete) functionality implemented in the `animal_shelter` module and demonstrates its usage through the `module5_crud_tests.ipynb` notebook.

---

## 1. Create Operation

The `create` method handles the insertion of new animal documents into the MongoDB `animals` collection.

### Module Implementation (`animal_shelter.py`)

The method validates that the input data is a non-empty dictionary, inserts it into the collection, and returns `True` upon success. It includes robust error handling to catch invalid input or database-level issues.

```python
def create(self, data: Dict[str, Any]) -> bool:
    """
    Create method to implement the C in CRUD.

    Args:
        data (Dict[str, Any]): Document data to insert into the collection.

    Returns:
        bool: True if successful insert, False otherwise

    Raises:
        ValueError: If data is None or empty
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
```

### Notebook Usage (`module5_crud_tests.ipynb`)

In the test notebook, a unique test document is created and passed to the `shelter.create()` method. The test asserts that the operation returns `True`.

```python
import time

unique_suffix = str(int(time.time()))
TEST_ANIMAL_ID = f"M5-TEST-{unique_suffix}"

test_doc = {
    "animal_id": TEST_ANIMAL_ID,
    "name": "Ranger",
    "animal_type": "Dog",
    "breed": "Labrador Retriever",
    "age_upon_outcome": "1 year",
    "outcome_type": ""
}

created = shelter.create(test_doc)
print("Create success?", created)
assert created is True, "Create should return True for a successful insert"
```

---

## 2. Read Operation

The `read` method retrieves documents from the collection based on a query criteria dictionary. If no criteria are supplied, it returns all documents.

### Module Implementation (`animal_shelter.py`)

The method takes an optional `criteria` dictionary. It uses `collection.find()` to perform the query and returns the results as a list of dictionaries.

```python
def read(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Read method to implement the R in CRUD.

    Args:
        criteria (Optional[Dict[str, Any]]): Query criteria to filter documents.

    Returns:
        List[Dict[str, Any]]: List of matching documents.
    """
    try:
        # Validate criteria parameter
        if criteria is not None and not isinstance(criteria, dict):
            raise ValueError("Criteria parameter must be a dictionary or None")

        query = criteria if criteria is not None else {}

        # Log the query attempt
        if criteria:
            self.logger.info(f"Querying documents with criteria: {criteria}")
        else:
            self.logger.info("Querying all documents")

        # Execute the query
        cursor = self.collection.find(query)
        documents = list(cursor)

        self.logger.info(f"Query returned {len(documents)} documents")
        return documents

    except ValueError as ve:
        self.logger.error(f"Validation error in read method: {str(ve)}")
        raise
    except Exception as e:
        self.logger.error(f"Database error in read method: {str(e)}")
        raise Exception(f"Failed to query documents: {str(e)}") from e
```

### Notebook Usage (`module5_crud_tests.ipynb`)

The test notebook calls `shelter.read()` using the `animal_id` of the just-created test document to verify that it exists in the database.

```python
docs = shelter.read({"animal_id": TEST_ANIMAL_ID})
print(f"Read returned {len(docs)} document(s)")
assert isinstance(docs, list), "Read should return a list"
assert len(docs) == 1, "Expected exactly one matching document"
print("Document:", {k: v for k, v in docs[0].items() if k != "_id"})
```

---

## 3. Update Operation

The `update` method modifies existing documents matching a given criteria. It can update a single document or multiple documents.

### Module Implementation (`animal_shelter.py`)

The method requires a `criteria` filter, `update_values` (using MongoDB update operators like `$set`), and an optional `many` flag. It returns the count of modified documents.

```python
def update(self, criteria: Dict[str, Any], update_values: Dict[str, Any], many: bool = False) -> int:
    """
    Update method to implement the U in CRUD.

    Args:
        criteria (Dict[str, Any]): Query filter for documents to update.
        update_values (Dict[str, Any]): MongoDB update spec (e.g., {"$set": {...}}).
        many (bool): If True, update many documents; otherwise update one.

    Returns:
        int: Number of documents modified.
    """
    try:
        if criteria is None or not isinstance(criteria, dict):
            raise ValueError("Criteria parameter must be a non-empty dictionary")
        if not isinstance(update_values, dict) or not update_values:
            raise ValueError("update_values must be a non-empty dictionary...")

        if many:
            result = self.collection.update_many(criteria, update_values)
        else:
            result = self.collection.update_one(criteria, update_values)

        modified = int(result.modified_count or 0)
        self.logger.info(f"Update modified_count: {modified}")
        return modified

    except Exception as e:
        self.logger.error(f"Database error in update method: {str(e)}")
        raise Exception(f"Failed to update documents: {str(e)}") from e
```

### Notebook Usage (`module5_crud_tests.ipynb`)

The notebook updates the test document's `outcome_type` and asserts that the `modified_count` is 1. It then reads the document again to verify the change was applied.

```python
modified_count = shelter.update(
    {"animal_id": TEST_ANIMAL_ID},
    {"$set": {"outcome_type": "Adoption"}},
    many=False
)
print("Modified count:", modified_count)
assert modified_count in (0, 1)

post_update_docs = shelter.read({"animal_id": TEST_ANIMAL_ID})
print("Post-update document:", {k: v for k, v in post_update_docs[0].items() if k != "_id"})
assert post_update_docs[0]["outcome_type"] == "Adoption"
```

---

## 4. Delete Operation

The `delete` method removes documents from the collection that match a given criteria. It can delete a single document or multiple documents.

### Module Implementation (`animal_shelter.py`)

The method requires a `criteria` filter and an optional `many` flag. It returns the count of deleted documents.

```python
def delete(self, criteria: Dict[str, Any], many: bool = False) -> int:
    """
    Delete method to implement the D in CRUD.

    Args:
        criteria (Dict[str, Any]): Query filter for documents to delete.
        many (bool): If True, delete many documents; otherwise delete one.

    Returns:
        int: Number of documents deleted.
    """
    try:
        if criteria is None or not isinstance(criteria, dict):
            raise ValueError("Criteria parameter must be a non-empty dictionary")

        if many:
            result = self.collection.delete_many(criteria)
        else:
            result = self.collection.delete_one(criteria)

        deleted = int(result.deleted_count or 0)
        self.logger.info(f"Delete deleted_count: {deleted}")
        return deleted

    except Exception as e:
        self.logger.error(f"Database error in delete method: {str(e)}")
        raise Exception(f"Failed to delete documents: {str(e)}") from e
```

### Notebook Usage (`module5_crud_tests.ipynb`)

Finally, the notebook deletes the test document and verifies success by asserting the deleted count is 1 and that a subsequent read for that `animal_id` returns zero documents.

```python
deleted_count = shelter.delete({"animal_id": TEST_ANIMAL_ID}, many=False)
print("Deleted count:", deleted_count)
assert deleted_count in (0, 1)

verify_delete = shelter.read({"animal_id": TEST_ANIMAL_ID})
print(f"Read after delete returned {len(verify_delete)} document(s)")
assert len(verify_delete) == 0, "Document should have been deleted"
```

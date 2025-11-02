"""
CS 340 - Module 5, Project 1: Full CRUD and Indexing Test Script

This script provides a command-line interface to validate the full CRUD
(Create, Read, Update, Delete) functionality and indexing for the AnimalShelter module.

It performs the following actions:
1. Sets up the Python path to locate the 'animal_shelter' module.
2. Configures database connection settings via environment variables.
3. Connects to the MongoDB database using the 'aacuser' credentials.
4. Ensures that recommended indexes are created on the 'animals' collection.
5. Executes an end-to-end test of the CRUD operations:
    - Creates a unique test document.
    - Reads the document to verify creation.
    - Updates the document to test modification.
    - Deletes the document to test removal.
6. Prints the results of each operation to the console.
"""

import sys
import os
import time
from pathlib import Path

# --- 1. System Path Bootstrap ---
# Ensure the project root containing 'animal_shelter' is importable.
try:
    candidate = Path.cwd()
    project_root = None
    # Search up to 6 levels for the project root
    for _ in range(6):
        if (candidate / "animal_shelter").is_dir():
            project_root = candidate
            break
        # A common case is running from a parent dir like 'm4-m5'
        if (candidate / "m4-m5" / "animal_shelter").is_dir():
            project_root = candidate / "m4-m5"
            break
        candidate = candidate.parent

    if project_root and str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"✅ Project root added to sys.path: {project_root}")
    elif not project_root:
        raise RuntimeError("Could not find the 'animal_shelter' directory.")

    from animal_shelter.animal_shelter import AnimalShelter
except ImportError as e:
    print(f"❌ Error: Could not import AnimalShelter. Details: {e}")
    print("Ensure the 'animal_shelter' directory is in the correct path.")
    sys.exit(1)
except RuntimeError as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

def run_crud_tests():
    """
    Executes the full suite of CRUD tests against the AnimalShelter module.
    """
    # --- 2. Configuration ---
    # Load configuration from environment variables with sensible defaults.
    print("\n" + "="*50)
    print("⚙️  Loading Configuration...")
    # REQUIRED for grading: use the aacuser account created in Module 3
    os.environ.setdefault("AAC_USER", "aacuser")
    os.environ.setdefault("AAC_PASS", "SECRET") # Replace with your actual aacuser password
    os.environ.setdefault("AAC_DATABASE", "aac")
    os.environ.setdefault("AAC_COLLECTION",   "animals")
    os.environ.setdefault("MONGO_HOST", os.getenv("MONGODB_HOST", "localhost"))
    os.environ.setdefault("MONGO_PORT", os.getenv("MONGODB_PORT", "27017"))

    print(f"   - AAC_DATABASE:   {os.getenv('AAC_DATABASE')}")
    print(f"   - AAC_COLLECTION: {os.getenv('AAC_COLLECTION')}")
    print(f"   - MONGO_HOST:     {os.getenv('MONGO_HOST')}")
    print(f"   - MONGO_PORT:     {os.getenv('MONGO_PORT')}")
    print(f"   - Using aacuser:  {os.getenv('AAC_USER') == 'aacuser'}")
    print("="*50)

    # Use a 'with' statement to ensure the connection is always closed.
    try:
        with AnimalShelter() as shelter:
            print("\n✅ Successfully connected to the database.")
            stats = shelter.get_collection_stats()
            print("   - Initial Collection Stats:")
            for key, value in stats.items():
                print(f"     - {key}: {value}")

            # --- 3. Ensure Indexes ---
            print("\n" + "="*50)
            print("🛡️  Ensuring database indexes...")
            shelter.ensure_indexes()
            print("   - Indexes ensured successfully.")
            print("="*50)

            # --- 4. CRUD Test Cycle ---
            print("\n🧪 Starting CRUD Test Cycle...")

            # Generate a unique ID for this test run to avoid collisions.
            unique_suffix = str(int(time.time()))
            TEST_ANIMAL_ID = f"PYTEST-{unique_suffix}"
            test_doc = {
                "animal_id": TEST_ANIMAL_ID,
                "name": "PythonTestRanger",
                "animal_type": "Dog",
                "breed": "Test Retriever",
                "age_upon_outcome": "1 test year",
                "outcome_type": "Testing"
            }

            # --- CREATE ---
            print("\n--- CREATE Operation ---")
            created = shelter.create(test_doc)
            assert created is True, "Create should return True for a successful insert"
            print(f"✅ Create success: {created}")

            # --- READ ---
            print("\n--- READ Operation ---")
            docs = shelter.read({"animal_id": TEST_ANIMAL_ID})
            assert isinstance(docs, list), "Read should return a list"
            assert len(docs) == 1, "Expected exactly one matching document"
            print(f"✅ Read success: Returned {len(docs)} document(s).")
            # Hide ObjectId for cleaner output
            print("   - Document:", {k: v for k, v in docs[0].items() if k != "_id"})

            # --- UPDATE ---
            print("\n--- UPDATE Operation ---")
            update_query = {"animal_id": TEST_ANIMAL_ID}
            update_values = {"$set": {"outcome_type": "Adopted via Test"}}
            modified_count = shelter.update(update_query, update_values, many=False)
            assert modified_count in (0, 1), "Modified count should be 0 or 1"
            print(f"✅ Update success: Modified count is {modified_count}.")

            # Verify the update
            post_update_docs = shelter.read(update_query)
            assert post_update_docs[0]["outcome_type"] == "Adopted via Test"
            print("   - Verified update in database.")
            print("   - Post-update document:", {k: v for k, v in post_update_docs[0].items() if k != "_id"})

            # --- DELETE ---
            print("\n--- DELETE Operation ---")
            deleted_count = shelter.delete({"animal_id": TEST_ANIMAL_ID}, many=False)
            assert deleted_count in (0, 1), "Deleted count should be 0 or 1"
            print(f"✅ Delete success: Deleted count is {deleted_count}.")

            # Verify the delete
            verify_delete = shelter.read({"animal_id": TEST_ANIMAL_ID})
            assert len(verify_delete) == 0, "Document should have been deleted"
            print(f"   - Verified deletion: Read after delete returned {len(verify_delete)} documents.")

            print("\n" + "="*50)
            print("🎉 CRUD Test Cycle Complete!")
            print("="*50)

            # --- 5. Final Stats ---
            final_stats = shelter.get_collection_stats()
            print("\n📊 Final Collection Stats:")
            for key, value in final_stats.items():
                print(f"   - {key}: {value}")

    except ConnectionError as e:
        print(f"\n❌ DATABASE CONNECTION FAILED: {e}")
        print("   Please ensure MongoDB is running and accessible.")
        print("   Verify your connection settings in the .env file or environment.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)
    
    # Connection is automatically closed by the 'with' statement's __exit__ method.
    print("\n✅ Connection closed automatically.")


if __name__ == "__main__":
    run_crud_tests()

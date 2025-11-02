# Grazioso Salvare: Animal Shelter CRUD Module (Project One)

## 1. About the Project

This project delivers a Python module that implements full CRUD (Create, Read, Update, Delete) functionality for a MongoDB database containing the Austin Animal Center (AAC) outcomes dataset. It is designed to allow the Grazioso Salvare organization to programmatically interact with animal shelter data to identify suitable candidates for search-and-rescue training.

This document outlines the module's purpose, setup, usage, and provides demonstrations of its core features, fulfilling the requirements for CS 340 Project One.

### Technology Stack

-   **Docker & Docker Compose**: For creating a reproducible, containerized development environment.
-   **Python 3.11**: The core programming language for the module.
-   **PyMongo**: The official MongoDB driver for Python, chosen for its robust, low-level control and direct mapping to MongoDB's API.
-   **Jupyter Notebook**: Used for interactive testing and demonstration of the module's functionality.
-   **MongoDB**: The NoSQL database used for its flexible document-based storage.

---

## 2. Getting Started with Docker (Recommended)

This project is fully containerized using Docker, which is the recommended way to run it. This method simplifies setup by automatically configuring the database, running the data import, and managing all dependencies.

### Prerequisites

-   Docker and Docker Compose installed on your system.
-   The `aac_shelter_outcomes.csv` file placed in the `assets/` directory.

### Steps

1.  **Clone the Repository**
    ```bash
    git clone <url>  # doesn't exist because this was submitted to bright hub, so I never initialized a repo.
    cd <project-directory>
    ```

2.  **Configure Environment**
    Create a `.env` file from the template. The default values are already configured for the Docker environment, but you can customize the `AAC_PASS` if desired.
    ```bash
    cp env.example .env
    ```

3.  **Launch the Environment**
    Build and run all services (MongoDB, Mongo Express, and the Data Importer) in the background.
    ```bash
    docker-compose up -d --build
    ```
    On the first run, this command will:
    - Build the custom `data-importer` Docker image.
    - Start the MongoDB and Mongo Express services.
    - Automatically create the `aacuser` in MongoDB.
    - The `data-importer` service will wait for MongoDB to be ready and then automatically run the Python script to import the data from `assets/aac_shelter_outcomes.csv`.

You are now ready to use the system. You can connect to the database from your local machine on `localhost:27017` or use the Jupyter notebook to interact with the data.

---

## 3. Database Preparation

### Data Import (Automatic with Docker)

When using the Docker Compose setup, the data import is handled automatically by the `data-importer` service. It checks if data exists and, if not, populates the `animals` collection.

**Execution Screenshot (simulated `docker-compose up` log):**
```text
aac_mongodb_1          | MongoDB initialization complete
aac_data_importer_1    | 🚀 Starting AAC Data Importer...
aac_data_importer_1    | ⏳ Waiting for MongoDB to be ready...
aac_data_importer_1    | MongoDB is ready!
aac_data_importer_1    | 📁 Found CSV file, starting import...
aac_data_importer_1    | 🔄 Starting data import...
aac_data_importer_1    | 🎉 Import completed successfully!
```

### User Authentication (Automatic with Docker)

The `init-mongo.js` script, run by the MongoDB container on its first launch, automatically creates the `aacuser` with the necessary permissions on the `aac` database.

**Execution Screenshot (simulated `docker-compose up` log):**
```text
aac_mongodb_1          | ... creating user "aacuser" ...
aac_mongodb_1          | ... created user "aacuser" on "aac"
```

---

## 4. Module Usage & CRUD Demonstrations

The `animal_shelter.AnimalShelter` class is the primary interface for all database operations. The following demonstrations assume you are running the `module5_crud_tests.ipynb` notebook against the running Docker environment.

### Initialization

First, import and instantiate the class. It automatically connects to the database using the configured environment variables.
```python
from animal_shelter import AnimalShelter

# Instantiate the class to establish a connection
shelter = AnimalShelter()
```

### Create Operation

The `create()` method inserts a new document. It returns `True` on success.

**Code:**
```python
# Create a new animal document
new_animal = {
    "animal_id": "A1234567",
    "name": "Sparky",
    "animal_type": "Dog",
    "breed": "Golden Retriever",
    "age_upon_outcome": "1 year"
}
is_created = shelter.create(new_animal)
print(f"Document creation successful: {is_created}")
```
**Output Screenshot (simulated):**
```text
Document creation successful: True
```

### Read Operation

The `read()` method queries for documents using a filter. An empty filter returns all documents.

**Code:**
```python
# Read the document we just created
query_filter = {"animal_id": "A1234567"}
results = shelter.read(query_filter)

print(f"Found {len(results)} document(s).")
# Print the first result, excluding the internal _id for readability
if results:
    print({k: v for k, v in results[0].items() if k != "_id"})
```
**Output Screenshot (simulated):**
```text
Found 1 document(s).
{'animal_id': 'A1234567', 'name': 'Sparky', 'animal_type': 'Dog', 'breed': 'Golden Retriever', 'age_upon_outcome': '1 year'}
```

### Update Operation

The `update()` method modifies documents matching a filter. It returns the number of documents updated.

**Code:**
```python
# Update Sparky's record to note adoption
update_filter = {"animal_id": "A1234567"}
update_data = {"$set": {"outcome_type": "Adoption"}}
modified_count = shelter.update(update_filter, update_data)

print(f"Documents modified: {modified_count}")
```
**Output Screenshot (simulated):**
```text
Documents modified: 1
```

### Delete Operation

The `delete()` method removes documents matching a filter. It returns the number of documents deleted.

**Code:**
```python
# Remove the test document
delete_filter = {"animal_id": "A1234567"}
deleted_count = shelter.delete(delete_filter)

print(f"Documents deleted: {deleted_count}")
```
**Output Screenshot (simulated):**
```text
Documents deleted: 1
```

---

## 5. Alternative: Manual Setup

If you cannot use Docker, you can set up the project manually.

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run MongoDB**
    Ensure a MongoDB instance is running and accessible.
3.  **Import Data Manually**
    ```bash
    mongoimport --host <host> --port <port> --username <user> --password <pass> --authenticationDatabase admin --db aac --collection animals --file ./assets/aac_shelter_outcomes.csv --type csv --headerline
    ```
4.  **Run Tests**
    Execute the Jupyter notebook (`notebooks/module5_crud_tests.ipynb`) to test functionality.

---

## 6. Conclusion

This project provides a robust, reusable, and containerized environment for performing all required CRUD operations on the Grazioso Salvare animal shelter database. It follows industry best practices for security, error handling, and code structure, laying a strong foundation for future development.

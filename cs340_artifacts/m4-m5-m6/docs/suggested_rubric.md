### **Refactored: CS 340 Module Four Milestone**

#### **Project Overview**

The goal of this milestone is to develop a reusable Python module that provides **Create** and **Read** (C, R) functionality for a MongoDB database. This module will serve as the data access layer for future projects, including the Project Two dashboard. You will implement the `AnimalShelter` class with methods to insert new documents and query existing documents from the Austin Animal Center (AAC) database.

#### **Learning Objectives**

Upon successful completion of this milestone, you will be able to:

* Implement the **Create** and **Read** operations of CRUD using Python.
* Utilize the PyMongo library to interact with a MongoDB instance.
* Apply Object-Oriented Programming (OOP) principles to create a modular and reusable database class.
* Write a separate script to test the functionality of your Python module.
* Adhere to software development best practices, including clear naming, exception handling, and code commenting.

#### **Prerequisites**

Before you begin, ensure you have completed the following from previous modules:

1.  **MongoDB User Account:** The `aacuser` account must be created with the proper permissions for the `AAC` database.
2.  **Data Import:** The `aac_shelter_outcomes.csv` dataset must be imported into the `AAC` database under the `animals` collection using the `mongoimport` tool.

---

### **Assignment Requirements**

This assignment is divided into two parts: building the Python module and creating a script to test it.

#### **Part 1: The `AnimalShelter` CRUD Module (`.py` file)**

You will create a Python file (e.g., `AnimalShelter.py`) containing a class named `AnimalShelter`. This class will manage all database interactions.

**Class: `AnimalShelter`**

* **`__init__(self)` Method (Initialization):**
    * Establishes a connection to the MongoDB server using the connection parameters (`USER`, `PASS`, `HOST`, `PORT`).
    * Specifies the target database (`DB`) and collection (`COL`).
    * Handles authentication for the `aacuser`.

* **`create(self, data)` Method (Create):**
    * **Purpose:** Inserts a new document into the `animals` collection.
    * **Parameters:**
        * `data`: A Python `dict` object containing the key-value pairs of the document to be inserted.
    * **Logic:**
        1.  Validate that the `data` parameter is not `None` and is a dictionary. If not, the method should not attempt to insert and should return `False`.
        2.  Use the `insert_one()` method from PyMongo to add the document to the collection.
        3.  Implement exception handling (e.g., a `try...except` block) to catch potential errors during the database operation.
    * **Return Value:**
        * Returns `True` if the insert operation is successfully acknowledged by the database.
        * Returns `False` if the input `data` is invalid or if the database insert fails.

* **`read(self, query)` Method (Read):**
    * **Purpose:** Retrieves documents from the `animals` collection that match a specific query.
    * **Parameters:**
        * `query`: A Python `dict` object representing the search criteria (e.g., `{'animal_type': 'Dog'}`).
    * **Logic:**
        1.  Validate that the `query` parameter is a dictionary. If not, return an empty list.
        2.  Use the `find()` method from PyMongo to search the collection. **Do not use `find_one()`**.
        3.  The `find()` method returns a cursor object. You must iterate through this cursor to access the documents.
        4.  Collect all matching documents into a Python `list`.
        5.  Implement exception handling to catch potential database errors.
    * **Return Value:**
        * Returns a `list` containing all found documents.
        * Returns an empty `list` (`[]`) if no documents are found or if an error occurs.

#### **Part 2: The Testing Script (`.ipynb` file)**

You will create a Jupyter Notebook to test the functionality of your `AnimalShelter` module. This script will demonstrate that your `create` and `read` methods work as expected.

**Testing Procedure:**

1.  **Import:** Import your `AnimalShelter` class from your `.py` module.
2.  **Instantiate:** Create an instance of your `AnimalShelter` class.
3.  **Test Create:**
    * Define a sample animal document as a Python dictionary (e.g., `new_animal_data = {...}`).
    * Call the `create()` method with this data.
    * Verify that the method returns `True`.
4.  **Test Read:**
    * Call the `read()` method using a query that should find the document you just created.
    * Verify that the returned result is a list containing the newly added document.
    * Print the results to the notebook output to show success.
5.  **Screenshots:** Take screenshots of your Jupyter Notebook, clearly showing the code cells and their successful execution outputs. These will be included in your documentation.

#### **Code Quality and Best Practices**

Your code will be evaluated on its adherence to industry-standard best practices:

* **Naming Conventions:** Use clear and descriptive names for variables, methods, and the class (e.g., `AnimalShelter`, `new_animal_data`).
* **In-line Comments:** Use comments to explain complex or non-obvious sections of your code. The `__init__` method is a good place for initial setup comments. Docstrings for the class and each method are highly recommended to explain their purpose, parameters, and return values.
* **Exception Handling:** Wrap database operations in `try...except` blocks to gracefully handle connection errors or failed queries without crashing the program.

---

### **Submission Checklist**

Submit the following items:

1.  **Python Module:** Your `.py` file containing the `AnimalShelter` class.
2.  **Jupyter Notebook:** Your `.ipynb` testing script.
3.  **Documentation:** A Microsoft Word document containing screenshots of the successful execution of your testing script.

---

### **Refactored Grading Rubric**

| Criteria | Exemplary (100%) | Proficient (85%) | Needs Improvement (70%) | Not Evident (0%) | Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Create Method Implementation** | Method correctly inserts a document, handles invalid input (`None` or non-dict), uses exception handling, and returns `True` on success and `False` on failure. Code is well-commented. | Method correctly inserts a document and returns a boolean value, but may have minor omissions in input validation or exception handling. | Method attempts to insert a document but has functional bugs, does not return the correct data type (`True`/`False`), or lacks required components like input validation. | The `create` method is not attempted or is non-functional. | 30% |
| **Read Method Implementation** | Method correctly queries using `find()`, properly handles the cursor, returns a list of all matching documents, handles invalid input, and uses exception handling. Code is well-commented. | Method correctly queries for documents and returns a list, but may be missing robust exception handling or cursor management is not perfectly efficient. | Method attempts to query but uses `find_one()`, returns an incorrect data type, fails to handle the cursor correctly, or has functional bugs. | The `read` method is not attempted or is non-functional. | 30% |
| **Testing Script & Verification** | Jupyter Notebook script successfully imports the module, instantiates the class, and executes tests for both `create` and `read`. The output clearly demonstrates that both methods work as specified. | The script tests both methods, but the tests may be incomplete or the output is not perfectly clear in demonstrating success (e.g., doesn't print the read result). | The script is incomplete, contains errors, fails to import the module correctly, or only tests one of the two required methods. | No testing script is provided or the script fails to run. | 40% |
| **Total** | | | | | **100%** |

***

### **Why This Refactoring is an Improvement**

* **Clear, Action-Oriented Structure:** The document is now organized into logical sections (`Overview`, `Requirements`, `Rubric`) that mirror a professional software development workflow.
* **Specific, Unambiguous Requirements:** Vague phrases like "data type acceptable to the MongoDB driver" have been replaced with precise terms like "a Python `dict` object." The expected logic for each method (validation, error handling, return values) is explicitly defined.
* **Logical Flow:** The requirements for the module (`.py` file) and the testing script (`.ipynb` file) are separated into `Part 1` and `Part 2`, making it easy to focus on one task at a time.
* **Constructive Rubric:** The new rubric provides a clear, multi-level performance standard for each requirement. The criteria in the rubric directly map to the tasks defined in the requirements section, leaving no doubt as to how you will be graded.
* **Emphasis on Best Practices:** Code quality is treated as a first-class citizen with its own dedicated section, reinforcing its importance.
# CS 340 Module Four Milestone Guidelines and Rubric

## Overview

You have learned that CRUD functionality is essential for interacting with databases. In Module Two, you gained practice using CRUD commands within the mongo shell. To develop a web application that connects a client-side user interface (such as a dashboard) to a database, it will help to develop a portable Python module that enables CRUD functionality for this data connection.

This milestone will help you begin creating a Python module that enables **create** and **read** functionality. You will finish developing the update and delete functionality for your Project One submission. You will eventually use this Python module to connect the user-interface component to the database component of your dashboard in Project Two.

> **Note:** This milestone requires you to use the "aacuser" account and password that you set up back in the Module Three milestone. If you did not successfully complete that milestone, follow the steps in Part II of the Module Three milestone to set up the "aacuser" account before beginning this milestone.

## Prompt

You will complete the readings for this module and then implement the fundamental operations of creating and reading documents (the **C** and **R** of CRUD) in Python. You will use the PyMongo driver to create CRUD functional access to your document collection.

### Step 1: Data Import

Upload the Austin Animal Center (AAC) Outcomes data set into MongoDB by importing a CSV file using the appropriate MongoDB import tool:

- **File Location:** `/usr/local/datasets/` directory in Apporto
- **Filename:** `aac_shelter_outcomes.csv`
- **Database Name:** `AAC`
- **Collection Name:** `animals`

Complete the import using the `mongoimport` tool, and take screenshots of both the import command and its execution.

> **Note:** If you completed the Module Three milestone, you have already completed this step.

### Step 2: Python Module Development

Develop a Python module in a `.py` file using object-oriented programming methodology to enable **create** and **read** functionality for the database. Other Python scripts must be able to import your Python code as a module to support code reusability.

Develop a CRUD class that, when instantiated, provides the following functionality:

#### Create Method
- **Purpose:** Inserts a document into a specified MongoDB database and collection
- **Input:** A set of key/value pairs in the data type acceptable to the MongoDB driver insert API call
- **Return:** `True` if successful insert, else `False`

#### Read Method
- **Purpose:** Queries for documents from a specified MongoDB database and collection
- **Input:** Key/value lookup pair to use with the MongoDB driver find API call
- **Return:** Result in a list if the command is successful, else an empty list

> **Important:** Be sure to use `find()` instead of `find_one()` when developing your method. **Hint:** You must work with the MongoDB cursor returned by the `find()` method.

As you develop your code, be sure to use industry standard best practices such as:
- Proper naming conventions
- Exception handling
- In-line comments

Doing so will ensure that your code is easy to read and reusable for future projects.

### Sample Code Template

Use the following sample code to get started. The authentication to MongoDB is in the initialization method for the CRUD class:

```python
from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        USER = 'aacuser'
        PASS = 'SECRET'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 31580
        DB = 'aac'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

    # Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            self.database.animals.insert_one(data)  # data should be dictionary            
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    # Create method to implement the R in CRUD.
```

### Step 3: Testing Script

Create a Python testing script in Jupyter Notebooks that:

1. Imports your CRUD Python module
2. Calls and tests the **create** and **read** instances of CRUD functionality
3. Uses the username and password for the "aacuser" account for authentication when instantiating the class

This script should be created in a separate Jupyter Notebook (`.ipynb`) file and should import and instantiate an object from your CRUD library to affect changes in MongoDB. After creating your script, execute it in Jupyter Notebook and take screenshots of the commands and their execution.

## What to Submit

For your submission, you must include:

1. **Code Files:**
   - Python module (`.py` file)
   - Python testing script (`.ipynb` file)

2. **Documentation:**
   - Microsoft Word document with screenshots from Step 3

## Module Four Milestone Rubric

| Criteria | Meets Expectations (100%) | Partially Meets Expectations (70%) | Does Not Meet Expectations (0%) | Value |
|----------|---------------------------|-----------------------------------|--------------------------------|-------|
| **Create Function** | Develops a method that inserts a document into a specified MongoDB database and collection and applies industry standard best practices such as naming conventions, exception handling, and in-line comments | Shows progress toward meeting expectations, but with errors or omissions; areas for improvement may include developing the create function or applying industry standard best practices | Does not attempt criterion | 30% |
| **Read Function** | Develops a method that queries for documents from a specified MongoDB database and specified collection and applies industry standard best practices such as naming conventions, exception handling, and in-line comments | Shows progress toward meeting expectations, but with errors or omissions; areas for improvement may include developing the read function or applying industry standard best practices | Does not attempt criterion | 30% |
| **Python Testing Script** | Creates a Python testing script that imports a CRUD Python module to call and test the create and read instances of CRUD functionality | Shows progress toward meeting expectations, but with errors or omissions; areas for improvement may include creating the Python testing script | Does not attempt criterion | 40% |
| **Total** | | | | **100%** |
"""
AnimalShelter CRUD Operations Package
CS 340 Module Four Milestone

This package provides CRUD operations for the Austin Animal Center (AAC) 
animals collection using PyMongo.

Requirements following EARS format:
- The AnimalShelter class shall provide CRUD operations for the animals collection
- When create() is called with valid data, the AnimalShelter shall insert the document and return True
- When create() is called with invalid data, the AnimalShelter shall raise an exception
- When read() is called with valid criteria, the AnimalShelter shall return matching documents as a list
- When read() is called with no criteria, the AnimalShelter shall return all documents as a list
"""

from .animal_shelter import AnimalShelter
from .data_importer import AACDataImporter

__version__ = "1.0.0"
__author__ = "Dave Mobley"
__email__ = "david.mobley@snhu.edu"

__all__ = [
    "AnimalShelter",
    "AACDataImporter"
] 
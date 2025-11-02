# AnimalShelter CRUD Operations - CS 340 Module Four Milestone

## Overview

This project implements CRUD operations for the Austin Animal Center (AAC) animals collection using PyMongo. It follows the Module Four milestone rubric requirements exactly.

## MongoDB Data Import Process

### Import Using mongoimport

This project demonstrates importing the Austin Animal Center (AAC) Outcomes dataset into MongoDB using the `mongoimport` tool. Place the CSV in `assets/aac_shelter_outcomes.csv` or provide an explicit path.

#### Example Command

```bash
mongoimport --host localhost --port 27017 \
  --db AAC --collection animals \
  --file assets/aac_shelter_outcomes.csv \
  --type csv --headerline
```

#### Verification Commands

1. Start a MongoDB shell:
   ```bash
   mongosh
   ```
2. Switch to the AAC database:
   ```javascript
   use AAC
   ```
3. Verify collection exists:
   ```javascript
   show collections
   ```
4. Count documents:
   ```javascript
   db.animals.countDocuments()
   ```
5. Inspect a sample document:
   ```javascript
   db.animals.findOne()
   ```

#### Import Process Details

**Database Configuration:**
- Database Name: `AAC`
- Collection Name: `animals`
- Authentication Database (if applicable): `admin`

**CSV File Specifications:**
- Source: `assets/aac_shelter_outcomes.csv` (or a provided path)
- Format: CSV with header row
- Import Method: `mongoimport` with `--headerline`

**Data Validation:**
- No duplicate records introduced during import
- Data integrity preserved
- Optional indexes recommended for query performance

#### Alternative Import Methods

The project also provides Python-based import functionality using the `AACDataImporter` class, which offers:

- Data validation and cleaning
- Batch processing for large datasets
- Duplicate detection and prevention
- Detailed import statistics and reporting
- Error handling and recovery

**Python Import Command:**
```bash
python import_aac_data.py
```

## Quick Start

### Local Development Setup

1. **Navigate to project directory**
   ```bash
   cd m4
   ```

2. **Create and activate virtual environment**
   ```bash
   # Option 1: Create new virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set up environment (Optional)**
   ```bash
   cp env.example .env
   # Edit .env if you need to customize settings
   ```

5. **Get CSV data (Optional)**
   ```bash
   ./scripts/get_csv_data.sh
   ```

6. **Start MongoDB and import data**
   ```bash
   docker-compose up -d
   ```

**Note**: The data importer will automatically run when you start the containers. If you have the CSV file in `assets/aac_shelter_outcomes.csv`, it will be imported automatically.

## Usage Examples

### Basic CRUD Operations

```python
from animal_shelter import AnimalShelter

# Create connection
shelter = AnimalShelter()

# Create a new animal record
animal_data = {
    "animal_id": "A123456",
    "name": "Buddy",
    "animal_type": "Dog",
    "breed": "Golden Retriever"
}
result = shelter.create(animal_data)

# Read all animals
all_animals = shelter.read()

# Read specific animals
dogs = shelter.read({"animal_type": "Dog"})

# Close connection
shelter.close_connection()
```

### Import AAC Data

**Automatic Import (Docker)**: Data is imported automatically when containers start if `assets/aac_shelter_outcomes.csv` exists.

**Manual Import**:
```bash
# Check if data already exists
python import_aac_data.py --check-only

# Import the full dataset (will skip if already exists)
python import_aac_data.py

# Force reimport (overwrites existing data)
python import_aac_data.py --force

# Custom batch size
python import_aac_data.py --batch-size 500
```

**CSV File Locations**:
- `assets/aac_shelter_outcomes.csv` (Docker automatic import)
- Current directory (`./`)
- `data/` subdirectory

**Smart Import Features**:
- Automatically detects existing data to prevent duplicates
- Provides detailed status information
- Supports force reimport for data updates
- Configurable batch sizes for performance tuning

### Run Tests

```bash
# Unit tests
python -m pytest test_animal_shelter.py -v

# Jupyter notebook tests
python -m jupyter notebook test_animal_shelter.ipynb
```

## Project Structure

```
m4/
├── animal_shelter/            # Main package
│   ├── __init__.py 
│   ├── animal_shelter.py      # CRUD operations
│   └── data_importer.py       # Data import
├── scripts/                   # Utility scripts
│   ├── get_csv_data.sh        # CSV data helper
│   ├── startup.sh             # Container startup script
├── assets/                    # Data files
│   └── aac_shelter_outcomes.csv (optional)
├── docs/                      # Documentation
├── test_animal_shelter.py     # Unit tests
├── test_animal_shelter.ipynb  # Jupyter tests
├── import_aac_data.py         # Import script
├── docker-compose.yml         # Docker services
├── Dockerfile.importer        # Data importer container
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Troubleshooting

### MongoDB Connection Issues

### Python 3.13 Issues
If you encounter pandas installation errors:
```bash
pip install -r requirements-py313.txt
```

### CSV File Not Found
The system automatically searches for `aac_shelter_outcomes.csv` in:
- `assets/aac_shelter_outcomes.csv` (Docker automatic import)
- Current directory
- `data/` subdirectory

**To import data manually:**
```bash
# Place the CSV file in assets/ for automatic Docker import, or run:
python import_aac_data.py
```

## Requirements Implementation Status

**Create Function (30%)**: Complete implementation with validation and error handling  
**Read Function (30%)**: Complete implementation with criteria support and list returns  
**Python Testing Script (40%)**: Comprehensive Jupyter notebook with EARS documentation

## Environment Variables

Copy `env.example` to `.env` to customize settings:

```bash
cp env.example .env
```

### Local Development
**Key Variables:**
- `AAC_USER` / `AAC_PASS`: MongoDB credentials
- `MONGODB_HOST` / `MONGODB_PORT`: MongoDB connection
- `AAC_DATABASE` / `AAC_COLLECTION`: Database and collection names
- `BATCH_SIZE`: Data import batch size
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `CSV_SEARCH_PATHS`: Comma-separated paths to search for CSV file

###
### Project Two: Dashboard (Grazioso Salvare)

#### Overview

This phase delivers a client-facing dashboard that interfaces with the AAC MongoDB database to help Grazioso Salvare identify dogs for training. The dashboard follows the MVC pattern:
- **Model**: MongoDB accessed via the `AnimalShelter` CRUD class
- **View**: Dash components (table, chart, map, controls)
- **Controller**: Dash callbacks that execute CRUD reads and update the UI

The dashboard includes:
- **Interactive Filters**: Rescue categories per specification
  - Reset (All)
  - Water Rescue
  - Mountain or Wilderness Rescue
  - Disaster or Individual Tracking
- **Interactive Data Table**: Sortable, paginated, single-row selection
- **Geolocation Map**: Centers and marks the selected animal (via `dash-leaflet`) with base-layer switching, marker clustering, auto-bounds, and scale control
- **Chart (User-Selectable)**: Bar, Pie, or Treemap of top breeds rendered with ECharts; premium styling
- **Branding**: Grazioso Salvare logo and a unique identifier (name)
- **Logo Link**: Logo is clickable and opens `https://www.snhu.edu` in a new tab

All widgets respond to filter changes. Table drives map selection.

#### How to Run (Reproducibility)

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure MongoDB has AAC data (use the provided importer or existing database)
   ```bash
   # Optional: load or verify data
   python import_aac_data.py --check-only
   python import_aac_data.py           # imports if needed
   ```
3. Launch Jupyter and open the notebook
   ```bash
   jupyter notebook notebooks/ProjectTwoDashboard.ipynb
   ```
4. (Optional) For large datasets, set a row cap to improve performance
   ```python
   # In the notebook environment before running, or set OS env
   # MAX_ROWS defaults to 2000
   ```
5. Run all cells. The Dash app starts in external mode. Open the provided URL.

#### Required Functionality (Screenshot Checklist)

Capture the following states (each with the logo and your unique identifier visible):
- Starting dashboard (controls, table, chart, map)
- After applying: Water Rescue
- After applying: Mountain or Wilderness Rescue
- After applying: Disaster or Individual Tracking
- Reset (returns to unfiltered state)

Placed screenshots in `submissions/screenshots/` and reference them in your submission.

#### Tools and Rationale

- **MongoDB + PyMongo**: Flexible schema for AAC data; excellent Python interoperability; efficient reads with projections and indexes; easy geospatial-friendly storage of lat/lon fields.
- **Dash**: Unifies view and controller in Python; reactive callbacks; production-friendly components; simple deployment.
- **ECharts (dash-echarts)**: High-quality consulting-grade visuals (Bar, Pie, Treemap) with crisp typography and layout; replaces Plotly in this phase.
- **dash-leaflet**: Lightweight, interactive map tiles and markers for geo-visualization.
- **Jupyter**: Iterative development and easy reproduction for grading and screenshots.

Useful references:
- Dash Docs: `https://dash.plotly.com/`
- ECharts: `https://echarts.apache.org/`
- dash-leaflet: `https://dash-leaflet.herokuapp.com/`
- MongoDB Docs: `https://www.mongodb.com/docs/`
- PyMongo: `https://pymongo.readthedocs.io/`

#### Steps Completed

1. Implemented `ProjectTwoDashboard.ipynb` following the Module Six style.
2. Connected to MongoDB via `AnimalShelter` and ensured indexes.
3. Implemented rescue-category filters and queries per specification.
4. Built interactive `DataTable` (sorting, pagination, single-row selection).
5. Added `dash-leaflet` map centered on selected animal; graceful fallbacks.
6. Added ECharts chart with user-selectable types (Bar, Pie, Treemap); premium styling.
7. Branded with logo and unique identifier.
8. Optimized performance: server-side projections, row limiting (`MAX_ROWS`), caching, pagination, virtualization, and index creation.
9. Enhanced map: base-layer switching (OSM/Toner/Terrain), marker clustering, auto-fit bounds, and scale control.

#### Challenges and Solutions

- **Slow Initial Load**: Avoided building a global DataFrame; used MongoDB projections with a row limit (`MAX_ROWS`), turned off client-side filtering, enabled pagination/virtualization, and ensured common indexes.
- **Chart Engine Swap (Plotly → ECharts)**: Replaced Plotly with ECharts (`dash-echarts`) for consulting-grade visuals and reliability; removed Plotly usage from the dashboard notebook.
- **Lat/Lon Column Variability**: Detected coordinate fields by sampling a document; hid columns in table; added map fallbacks when coordinates are missing.

#### File Pointers

- Dashboard Notebook: `notebooks/ProjectTwoDashboard.ipynb`
- CRUD Module: `animal_shelter/animal_shelter.py`
- Logo: `Grazioso Salvare Logo.png`
- Screenshots (suggested): `submissions/screenshots/`

#### Dependencies Update

- Added: `dash-echarts` (ECharts integration)
- Removed from code usage: Plotly (no Plotly imports remain in the dashboard notebook)
- Note: `dash` and `dash-leaflet` remain required for the app and map

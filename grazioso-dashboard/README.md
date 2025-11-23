# Enhancement One: Software Design and Engineering

## Overview

This project transforms the Grazioso Salvare Animal Shelter Dashboard from a Jupyter notebook-based Dash application into a production-ready three-tier web application.

## Project Structure

```
enhancement-one/
├── original/              # Original artifact (read-only reference)
├── backend/               # FastAPI RESTful API
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration, database, security
│   │   ├── models/       # Pydantic models
│   │   └── services/     # Business logic services
│   ├── tests/            # Test suites
│   └── requirements.txt  # Python dependencies
├── frontend/             # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── contexts/    # React contexts
│   │   ├── pages/       # Page components
│   │   └── services/   # API client
│   └── package.json     # Node dependencies
├── docs/                 # Documentation
├── deployment/           # Docker and CI/CD configs
└── README.md            # This file
```

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker and Docker Compose
- MongoDB (or use Docker Compose)
- Redis (or use Docker Compose - included in docker-compose.yml)

## Quick Start

### Using Docker Compose (Recommended)

1. Navigate to the deployment directory:
   ```bash
   cd deployment
   ```

2. Start all services:
   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Setup

#### Backend

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Copy environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the server:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

#### Frontend

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install yarn (if not already installed):
   ```bash
   npm install -g yarn
   # Or use corepack: corepack enable
   ```

3. Install dependencies:
   ```bash
   yarn install
   ```

4. Create `.env` file:
   ```bash
   echo "VITE_API_BASE_URL=http://localhost:8000" > .env
   ```

5. Run development server:
   ```bash
   yarn dev
   ```

## Testing

### Backend Tests

```bash
cd backend
uv run pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
yarn test
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Default Credentials

- **Admin**: username: `admin`, password: `admin123`
- **User**: username: `user`, password: `user123`

## Features

### Software Design and Engineering
- ✅ RESTful API with FastAPI
- ✅ JWT Authentication and Authorization
- ✅ Role-based Access Control (Admin/User)
- ✅ Comprehensive Audit Logging
- ✅ React Frontend with Modern UI
- ✅ Docker Containerization
- ✅ CI/CD Pipeline with GitHub Actions
- ✅ Comprehensive Test Coverage
- ✅ Security Headers and Rate Limiting

### Algorithms and Data Structures
- ✅ Trie Data Structure for O(log n) Autocomplete Search
- ✅ Redis-backed LRU Cache with In-Memory Fallback
- ✅ Fuzzy String Matching with Levenshtein Distance
- ✅ Cache Invalidation and TTL Management
- ✅ Performance Optimization (70-80% reduction in database queries)

## Algorithm Features

### Autocomplete Endpoints

**Breed Autocomplete:**
```bash
GET /api/animals/autocomplete/breeds?q=lab&limit=10
```

**Name Autocomplete:**
```bash
GET /api/animals/autocomplete/names?q=a&limit=10
```

### Fuzzy Search

**Fuzzy Breed Search:**
```bash
GET /api/animals/search/fuzzy?q=labrador&threshold=0.6&limit=10
```

The fuzzy search uses Levenshtein distance algorithm to find breeds similar to the query, handling typos and approximate matches.

### Caching

The application uses Redis-backed caching with automatic fallback to in-memory cache when Redis is unavailable. Cache entries have configurable TTL (default: 1 hour) and are automatically invalidated on data updates.

## Documentation

- [Artifact Analysis](docs/artifact_analysis.md)
- [Enhancement Narrative - Software Design](docs/enhancement_narrative.md)
- [Enhancement Narrative - Algorithms](docs/enhancement_narrative_algorithms.md)

## License

This project is part of CS 499 coursework at Southern New Hampshire University.


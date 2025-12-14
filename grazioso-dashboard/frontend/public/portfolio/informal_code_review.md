# Informal Code Review (Written)

## Audience and purpose

This is a written, informal code review intended for a peer or manager. It explains:

- What the system does
- Where the original artifact had constraints
- What was improved and why
- How the enhancements map to CS 499 outcomes

## Existing functionality (before enhancements)

The original artifact was a Jupyter Notebook application using Dash to present animal shelter data from MongoDB. Key features:

- Filter animals by rescue category using predefined rules
- Display a table of results
- Display map and breed analytics visualizations
- Perform basic CRUD-style reads with direct database access

The original structure worked for coursework, but it constrained maintainability, deployment, and security.

## Code analysis: opportunities for improvement

### Architecture and maintainability

- Monolithic notebook structure made modular reuse difficult.
- UI code and database logic were tightly coupled.

### Security and compliance

- No authentication or authorization.
- No audit trail for data operations.

### Scalability and performance

- Search patterns relied on basic matching.
- Database could be stressed by repeated reads.
- Limited support for efficient autocomplete/fuzzy search.

### Testing and quality

- Limited automated testing compared to what is expected in a professional environment.

## Enhancements implemented (what changed and why)

### Software engineering and design

- Migrated from notebook-based Dash app into a production-style three-tier architecture:
  - React frontend
  - FastAPI backend
  - MongoDB (and Redis-backed caching)

- Added security controls:
  - JWT authentication
  - Role-based authorization (admin vs user)
  - Rate limiting and security headers

- Added a service layer to keep code modular and testable.

### Algorithms and data structures

Enhancements were selected based on real user behavior (search and repeated reads):

- Trie-based autocomplete for breed/name prefix search
- Fuzzy search using edit-distance similarity
- Cache layer with TTL and invalidation to reduce repeated database reads

### Databases

- Implemented compound indexing strategy based on query patterns
- Added aggregation pipelines for analytics
- Added audit logging collection for traceability

## Evidence and alignment to CS 499 outcomes

### Outcome 1: Collaborative environments for decision making

- The UI + API design supports both end users and technical stakeholders.
- Audit logging supports accountable decision making and operational review.

### Outcome 2: Professional communication

- This written review + portfolio narratives explain the “why” behind the engineering.
- The portfolio presents original vs enhanced artifacts coherently.

### Outcome 3: Algorithmic solutions

- Trie and fuzzy matching improve search usability and performance.
- Caching reduces repeated workload while managing invalidation trade-offs.

### Outcome 4: Innovative techniques and tools

- FastAPI for typed endpoints and generated API documentation.
- React routing and state management for a modern UI.
- Container-friendly structure and automated tests.

### Outcome 5: Security mindset

- Authentication + RBAC + rate limiting reduce attack surface.
- Audit logging creates traceability for sensitive operations.

## How to run (high level)

- Backend: FastAPI service exposes `/api/*` endpoints.
- Frontend: React app provides both a public portfolio view and an authenticated dashboard.

## Closing summary

The enhanced artifact demonstrates the progression from a working prototype to an operationally credible system. The work intentionally emphasizes leadership-style concerns—trade-offs, maintainability, security posture, and stakeholder communication—while still providing concrete technical evidence in code and behavior.

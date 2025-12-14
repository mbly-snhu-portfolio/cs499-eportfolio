# Rubric Evidence Map (CS 499)

This page maps each course outcome to concrete evidence in this repository and portfolio.

## Outcome 1: Collaborative environments that support decision making

**Evidence in portfolio:**

- Written code review deliverable (peer/manager audience, review process checklist): `docs/informal_code_review.md`
- Audit logging supports operational decision making and accountability: backend audit log service and `audit_logs` collection
- Modular services support team development by reducing cross-cutting changes: `backend/app/services/animals/`

**Key repo locations:**

- `grazioso-dashboard/docs/informal_code_review.md`
- `grazioso-dashboard/backend/app/services/audit_service.py`
- `grazioso-dashboard/backend/app/services/animals/`

## Outcome 2: Professional-quality oral, written, and visual communication

**Evidence in portfolio:**

- Professional self-assessment (formal intro with required topics): `docs/professional_self_assessment.md`
- Artifact narrative (overall cohesion): `docs/artifact_narrative_overall.md`
- Three enhancement narratives (learning-focused reflection):
  - `docs/enhancement_narrative.md`
  - `docs/enhancement_narrative_algorithms.md`
  - `docs/enhancement_narrative_databases.md`
- Visual element included via architecture flowchart (mermaid) in `docs/informal_code_review.md`

## Outcome 3: Algorithmic principles and computing solutions with trade-offs

**Evidence in portfolio:**

- Trie-based autocomplete: `backend/app/utils/trie.py` and usage in service/search
- Fuzzy matching (edit distance similarity): `backend/app/utils/fuzzy_match.py`
- Caching strategy with TTL + invalidation trade-offs: `backend/app/utils/cache.py` and service integration
- Algorithms narrative with explicit complexity/trade-offs: `docs/enhancement_narrative_algorithms.md`

**Key repo locations:**

- `grazioso-dashboard/backend/app/utils/trie.py`
- `grazioso-dashboard/backend/app/utils/fuzzy_match.py`
- `grazioso-dashboard/backend/app/utils/cache.py`
- `grazioso-dashboard/backend/app/services/animals/search.py`
- `grazioso-dashboard/docs/enhancement_narrative_algorithms.md`

## Outcome 4: Innovative techniques, skills, and tools that deliver value

**Evidence in portfolio:**

- FastAPI backend with typed models and generated docs: `backend/app/main.py`, `backend/app/api/`
- React frontend with routing and component structure: `frontend/src/`
- Container/deployment structure: `deployment/docker-compose.yml`, Dockerfiles
- Automated tests and CI-ready structure: `backend/tests/`, `frontend/src/App.test.jsx`

## Outcome 5: Security mindset (anticipate exploits, mitigate vulnerabilities)

**Evidence in portfolio:**

- Authentication and authorization (JWT + RBAC): `backend/app/api/auth.py`, `backend/app/services/auth_service.py`
- Input validation via Pydantic models: `backend/app/models/`
- Audit logging (traceability): `backend/app/services/audit_service.py`
- Rate limiting and security headers: `backend/app/core/rate_limit.py`, `backend/app/core/security.py`
- Security discussed explicitly in narratives and self-assessment:
  - `docs/professional_self_assessment.md`
  - `docs/enhancement_narrative.md`
  - `docs/enhancement_narrative_databases.md`

---

## Quick links (GitHub Pages copies)

The GitHub Pages site serves the same content from:

- `grazioso-dashboard/frontend/public/portfolio/`

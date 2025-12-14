# Professional Self-Assessment

## Summary

I am a computer science graduate who approaches software as a socio-technical system: successful solutions require clear communication, strong engineering fundamentals, security awareness, and disciplined trade-off decisions. Throughout the CS program, I strengthened my ability to move from “it works” prototypes to solutions that can be maintained, audited, tested, and deployed.

This ePortfolio centers on an enhanced artifact—the **Grazioso Salvare Animal Shelter Dashboard**—because it showcases end-to-end growth: modern architecture, algorithmic performance improvements, and database engineering practices, all connected to real stakeholder needs.

## My strengths and how they show up in this portfolio

### Technical leadership and decision making

My focus is technical leadership: making decisions under constraints, documenting rationale, and aligning implementation details with business outcomes. In this artifact, I documented and implemented architectural changes (three-tier design, service boundaries, authentication, auditability), and I made deliberate trade-offs (performance vs. memory, consistency vs. caching, security vs. developer ergonomics).

### Communication for diverse audiences

A key part of leadership is communicating clearly for different audiences:

- **Non-technical stakeholders** need simple explanations of what the system does and why it matters.
- **Peers and managers** need the “why” behind decisions and evidence that risks were managed.
- **Developers** need readable code, modular structure, and test coverage.

This ePortfolio presents the original artifact, the enhanced implementation, and narratives that connect changes to outcomes and professional skills.

### Security mindset

I developed a security mindset by treating “security” as an architectural property instead of an add-on. In this artifact, that shows up in:

- **Authentication and authorization** (JWT + role-based access control)
- **Audit logging** (who did what, when, and from where)
- **Rate limiting and security headers** (defense in depth)
- **Validation and safe defaults** (Pydantic models and consistent error handling)

## Course outcomes alignment (evidence-driven)

### Outcome 1: Collaborative environments for decision making

I structured the solution so multiple audiences can use it:

- Users interact with a clear dashboard experience.
- Technical stakeholders can evaluate API behavior via OpenAPI docs.
- Developers can extend functionality through modular services.

The audit trail supports operational decision making by providing traceability and accountability.

### Outcome 2: Professional communication (written, visual, coherent)

This portfolio is intentionally organized:

- Self-assessment first (holistic narrative)
- Artifact overview (original vs enhanced)
- Enhancement narratives (software engineering, algorithms, databases)
- Written informal code review (replacement for video)

### Outcome 3: Algorithmic solutions and trade-offs

Algorithmic improvements were selected based on workload patterns:

- Trie-based autocomplete supports low-latency prefix search.
- Fuzzy matching supports human-friendly search behavior.
- Caching reduces repeated database reads while managing invalidation trade-offs.

### Outcome 4: Innovative techniques, tools, and delivery

The enhanced artifact uses modern, production-oriented tooling:

- FastAPI backend with structured services
- React frontend with routed pages
- Dockerized deployment patterns
- Automated testing and CI-ready structure

### Outcome 5: Security mindset and privacy of resources

Security and compliance needs drove design decisions:

- Principle of least privilege (admin vs user actions)
- Traceability (audit logging)
- Abuse resistance (rate limiting)
- Safe handling of errors and inputs

## Professional positioning

This ePortfolio reflects how I want to be positioned professionally: a technically strong, outcomes-focused engineer with leadership capability—someone who can translate requirements into secure, maintainable systems and communicate trade-offs and evidence to stakeholders.

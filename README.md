# TripleZero Ops

A multi-hazard incident-reporting and AI-assisted response-coordination platform, modelled on how Australian emergency services triage bushfires, floods, and other incidents.

Work in progress, Stage 1 build log starts here.

## Build Log

**24/09/2026**
- Designed and implemented a 3-table relational schema in PostgreSQL: `incidents`, `response_units`, and `dispatched_units` (a junction table modelling the many-to-many relationship between incidents and response units, since one incident can involve multiple units, and one unit can respond to multiple incidents over time).
- Added a custom `incident_status` ENUM type and a `CHECK` constraint on severity (1 to 4) to enforce data integrity at the database level.
- Built matching Pydantic models (`Incident`, `ResponseUnit`, `DispatchedUnit`) with validation, including bounded severity, enum-restricted status fields, and optional/nullable fields where appropriate. Verified both valid and invalid inputs behave correctly.
- Set up a dedicated `triplezero` database and a least-privilege application role (`triplezero_app`), scoped to only the permissions the app actually needs, rather than using the Postgres superuser.
- Moved all database credentials into a `.env` file (excluded from git) and built a `psycopg2`-based connection function that reads config from environment variables. Verified a live connection.

**04/10/2026**
- Built a Faker-based seed script (`app/seed.py`) generating realistic, domain-matched incidents (bushfire/flood/hazard/other) and response units.
- Implemented parameterized `insert_incident()` and `insert_response_unit()` functions in `app/db.py`, using psycopg2 to safely write to Postgres (no raw string SQL, protects against SQL injection).
- Fixed least-privilege role permissions: `triplezero_app` needed explicit GRANTs on sequences (not just tables) to use auto-incrementing IDs.
- Seeded the database with 30 incidents and 15 response units; verified end-to-end via row counts. Week 1 complete.

**12/10/2026**
- Built the FastAPI service with `GET /`, `GET /incidents`, `GET /incidents/{incident_id}` and `POST /incidents`. Pydantic validates every request and response, and Swagger docs are generated automatically at `/docs`.
- Decision: separate models for input (`IncidentCreate`), storage (`Incident`) and output (`IncidentOut`), so callers can't set server-controlled fields like `status` and `reported_at`, and responses include the Postgres-generated `id` (returned via `INSERT ... RETURNING id`).
- Decision: `db.py` returns `None` for a missing incident, and the endpoint turns that into a 404, which keeps the database layer independent of FastAPI. Non-integer ids get a 422 from FastAPI's validation before the function runs.
- Wrapped database work in `try/finally` so connections close even when a query fails, and installed `pytest` and `httpx` ready for API tests.


**14/10/2026**
- Added pytest tests for the API covering a success, a 404 for a missing incident, and a 422 for a non-integer id and for an out-of-range severity. Confirmed by row count that a rejected POST writes nothing to the database.
- Week 2 complete: REST API with validated input and output models, auto-generated docs, and automated tests.


## Known Limitations / TODO
- `response_units.callsign` has no UNIQUE constraint yet, so the seed script can generate duplicate callsigns (e.g. two separate rows both named "CFA Truck 7"). Should add a UNIQUE constraint once the schema is revisited.
- `response_units.status` is a plain VARCHAR rather than an ENUM, unlike `incidents.status`. Inconsistent on purpose-vs-accident - should be unified to an ENUM later.
- Tests run against the real `triplezero` database and assume incident 1 exists and 999 does not. There is no test for a valid `POST /incidents` yet, because it would insert real rows. Should move to a separate test database.
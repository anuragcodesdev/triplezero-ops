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


## Known Limitations / TODO
- `response_units.callsign` has no UNIQUE constraint yet, so the seed script can generate duplicate callsigns (e.g. two separate rows both named "CFA Truck 7"). Should add a UNIQUE constraint once the schema is revisited.
- `response_units.status` is a plain VARCHAR rather than an ENUM, unlike `incidents.status`. Inconsistent on purpose-vs-accident - should be unified to an ENUM later.
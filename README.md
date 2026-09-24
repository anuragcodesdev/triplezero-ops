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

Next up: a Faker-based seed script to populate realistic sample data.
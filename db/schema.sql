
DROP TABLE IF EXISTS dispatched_units, response_units, incidents CASCADE;
DROP TYPE IF EXISTS incident_status;

-- Custom type for incident status
CREATE TYPE incident_status AS ENUM ('reported', 'dispatched', 'contained', 'closed');

-- Incidents table
CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    incident_type VARCHAR(30) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    description VARCHAR(500),
    severity SMALLINT NOT NULL CHECK (severity BETWEEN 1 AND 4),
    status incident_status NOT NULL DEFAULT 'reported',
    reported_at TIMESTAMP NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMP
);

-- Response units table
CREATE TABLE response_units(
    id SERIAL PRIMARY KEY,
    callsign VARCHAR(50) NOT NULL,
    unit_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'available'
);

-- Junction table linking incidents and response units
CREATe TABLE dispatched_units (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER NOT NULL REFERENCES incidents(id),
    unit_id INTEGER NOT NULL REFERENCES response_units(id),
    dispatched_at TIMESTAMP NOT NULL DEFAULT NOW(),
    returned_at TIMESTAMP
);

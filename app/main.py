from fastapi import FastAPI
from app.db import get_all_incidents, insert_incident
from app.models import Incident, IncidentCreate, IncidentOut, IncidentStatus
from typing import List
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {"message": "TripleZero Ops API is running"}

@app.get("/incidents")
def show_incidents() -> List[Incident]:
    return get_all_incidents()

@app.post("/createincidents")
def create_incident(incident: IncidentCreate) -> IncidentOut:

    # Creating full incident object
    full_incident = Incident(
                            incident_type = incident.incident_type,
                            latitude = incident.latitude,
                            longitude = incident.longitude,
                            description = incident.description,
                            severity = incident.severity,
                            status = IncidentStatus.REPORTED,
                            reported_at = datetime.now()
                            )

    # Insert incident
    incident_id = insert_incident(incident=full_incident)

    # Given incident is inserted into table we have the Incident + id
    return IncidentOut(
        id=incident_id,
        incident_type=full_incident.incident_type,
        latitude=full_incident.latitude,
        longitude=full_incident.longitude,
        description=full_incident.description,
        severity=full_incident.severity,
        status=full_incident.status,
        reported_at=full_incident.reported_at,
    )
        
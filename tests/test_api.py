from fastapi.testclient import TestClient
from app.main import app
from app.models import IncidentCreate
from pydantic import ValidationError
import pytest

client = TestClient(app)

def test_get():
    response = client.get("/")
    assert response.status_code == 200

def test_invalid_parameter_incident():
    response = client.get("/incidents/abc")
    assert response.status_code == 422

def test_invalid_range_incident():
    response = client.get("/incidents/999")
    assert response.status_code == 404

def test_invalid_severity_incident_insert():
    with pytest.raises(ValidationError):
        IncidentCreate(
            incident_type="bushfire",
            latitude=-37.8136,
            longitude=145.1200,
            description=(
                "Bushfire spreading through dry grass near a residential property. "
                "Fire crews requested to assess the threat."),
            severity=9,
        )

def test_get_valid_incident():
    response = client.get("/incidents/1")
    assert response.status_code == 200 
    assert response.json()['id'] == 1

def test_post_incident_invalid_severity_returns_422():
    response = client.post(
    "/incidents",
    json={
        "incident_type": "bushfire",
        "latitude": -37.8136,
        "longitude": 145.1200,
        "description": (
            "Bushfire spreading through dry grass near a residential property. "
            "Fire crews requested to assess the threat."
        ),
        "severity": 9,
        },
    )
    assert response.status_code == 422
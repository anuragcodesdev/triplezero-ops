import random
from typing import Any

from faker import Faker

from app.models import (
    DispatchedUnit,
    Incident,
    IncidentStatus,
    ResponseUnit,
    UnitStatus,
)
from app.db import insert_incident, insert_response_unit

fake: Faker = Faker()

INCIDENT_TYPES: list[str] = ["bushfire", "flood", "hazard", "other"]

INCIDENTS: dict[str, list[tuple[str, int]]] = {
    "bushfire": [
        ("Small grass fire contained to a roadside area.", 1),
        ("Bushfire spreading through dry grass near a rural property.", 2),
        ("Large bushfire threatening multiple properties with residents being evacuated.", 3),
        ("Major bushfire rapidly spreading across multiple communities with widespread evacuations.", 4),
    ],
    "flood": [
        ("Minor localised flooding affecting a small section of roadway.", 1),
        ("Floodwater entering several properties after heavy rainfall.", 2),
        ("Significant flooding affecting multiple streets and requiring evacuations.", 3),
        ("Severe flooding across a large area with multiple communities isolated.", 4),
    ],
    "hazard": [
        ("Minor chemical spill contained within a small workplace area.", 1),
        ("Gas leak reported inside a commercial building with occupants evacuated.", 2),
        ("Large hazardous material spill requiring an emergency response and surrounding evacuation.", 3),
        ("Major hazardous material incident posing an immediate threat to a large populated area.", 4),
    ],
    "other": [
        ("Minor incident requiring a small emergency response.", 1),
        ("Incident requiring multiple emergency services with several people affected.", 2),
        ("Serious incident involving multiple casualties and requiring significant emergency resources.", 3),
        ("Major emergency involving widespread casualties and requiring a large-scale emergency response.", 4),
    ],
}

RESPONSE_UNITS: dict[str, list[str]] = {
    "fire truck": [
        "CFA Truck 7",
        "CFA Truck 12",
        "CFA Truck 23",
        "CFA Truck 31",
        "CFA Truck 45",
    ],
    "SES crew": [
        "SES Crew 2",
        "SES Crew 4",
        "SES Crew 9",
        "SES Crew 15",
        "SES Crew 21",
    ],
    "ambulance": [
        "Ambulance 101",
        "Ambulance 204",
        "Ambulance 317",
        "Ambulance 428",
        "Ambulance 512",
    ],
}


def random_incident_type() -> str:
    """
    Selects a random incident type from the supported list. This helps generate varied emergency scenarios for testing and seeding.

    params:
        :None None: No parameters are required.
    returns:
        :incident_type str: A random incident type from the application dataset.
    """
    return random.choice(INCIDENT_TYPES)


def random_victoria_coords() -> tuple[float, float]:
    """
    Generates a random set of Victorian coordinates for a simulated incident. The values stay within a practical latitude and longitude range for the state.

    params:
        :None None: No parameters are required.
    returns:
        :coords tuple: A latitude and longitude pair for a random Victorian location.
    """
    latitude: float = random.uniform(-38, -37)
    longitude: float = random.uniform(144, 146)

    return latitude, longitude


def random_incident_details(incident_type: str) -> tuple[str, int]:
    """
    Fetches a random description and severity for the supplied incident type. This supports realistic data generation for emergency scenarios.

    params:
        :incident_type str: The incident category to draw details for.
    returns:
        :details tuple: A description string and severity integer for the chosen incident type.
    """
    return random.choice(INCIDENTS[incident_type])


def generate_random_incident() -> Incident:
    """
    Builds a realistic incident object using randomised details and timestamps. It creates a valid Incident instance ready to be inserted into storage.

    params:
        :None None: No parameters are required.
    returns:
        :incident Incident: A populated Incident model instance.
    """
    incident_type: str = random_incident_type()
    latitude: float
    longitude: float
    latitude, longitude = random_victoria_coords()
    description: str
    severity: int
    description, severity = random_incident_details(incident_type)
    reported_at: Any = fake.date_time_this_year()

    return Incident(
        incident_type=incident_type,
        latitude=latitude,
        longitude=longitude,
        description=description,
        severity=severity,
        status=IncidentStatus.REPORTED,
        reported_at=reported_at,
    )


def generate_random_response_unit() -> ResponseUnit:
    """
    Creates a random response unit model with a valid callsign and status. This is used to seed realistic emergency service data.

    params:
        :None None: No parameters are required.
    returns:
        :response_unit ResponseUnit: A populated ResponseUnit model instance.
    """
    unit_type: str = random.choice(list(RESPONSE_UNITS))
    callsign: str = random.choice(RESPONSE_UNITS[unit_type])

    return ResponseUnit(
        callsign=callsign,
        unit_type=unit_type,
        status=UnitStatus.AVAILABLE,
    )


def bulk_insert_incident(num_incidents_to_insert: int) -> None:
    """
    Inserts the requested number of random incidents into the database. It generates and stores each incident sequentially until the target count is reached.

    params:
        :num_incidents_to_insert int: The number of incident records to create and insert.
    returns:
        :None None: This function does not return a value.
    """
    for _ in range(num_incidents_to_insert):
        incident: Incident = generate_random_incident()
        insert_incident(incident)


def bulk_insert_response_unit(num_response_units_to_insert: int) -> None:
    """
    Inserts the requested number of random response units into the database. It creates and saves each unit until the target count is reached.

    params:
        :num_response_units_to_insert int: The number of response unit records to create and insert.
    returns:
        :None None: This function does not return a value.
    """
    for _ in range(num_response_units_to_insert):
        response_unit: ResponseUnit = generate_random_response_unit()
        insert_response_unit(response_unit)
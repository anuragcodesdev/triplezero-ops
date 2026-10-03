import random

from faker import Faker

from app.models import (
    DispatchedUnit,
    Incident,
    IncidentStatus,
    ResponseUnit,
    UnitStatus,
)

fake = Faker()

INCIDENT_TYPES = ["bushfire", "flood", "hazard", "other"]

INCIDENTS = {
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

RESPONSE_UNITS = {
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


def random_incident_type():
    return random.choice(INCIDENT_TYPES)


def random_victoria_coords():
    latitude = random.uniform(-38, -37)
    longitude = random.uniform(144, 146)

    return latitude, longitude


def random_incident_details(incident_type):
    return random.choice(INCIDENTS[incident_type])


def generate_random_incident():
    incident_type = random_incident_type()
    latitude, longitude = random_victoria_coords()
    description, severity = random_incident_details(incident_type)
    reported_at = fake.date_time_this_year()

    return Incident(
        incident_type=incident_type,
        latitude=latitude,
        longitude=longitude,
        description=description,
        severity=severity,
        status=IncidentStatus.REPORTED,
        reported_at=reported_at,
    )


def generate_random_response_unit():
    unit_type = random.choice(list(RESPONSE_UNITS))
    callsign = random.choice(RESPONSE_UNITS[unit_type])

    return ResponseUnit(
        callsign=callsign,
        unit_type=unit_type,
        status=UnitStatus.AVAILABLE,
    )




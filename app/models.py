from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional, Annotated


class IncidentStatus(str, Enum):
    REPORTED = "reported"
    DISPATCHED = "dispatched"
    CONTAINED = "contained"
    CLOSED = "closed"

class UnitStatus(str, Enum):
    AVAILABLE = "available"
    DISPATCHED = "dispatched"
    OFF_DUTY = "off_duty"


class Incident(BaseModel):
    incident_type: str
    latitude: float
    longitude: float
    description: str
    severity: Annotated[int, Field(ge=1, le=4)]
    status: IncidentStatus
    reported_at: datetime
    closed_at: Optional[datetime] = None

class ResponseUnit(BaseModel):
    callsign: str
    unit_type: str
    status: UnitStatus = UnitStatus.AVAILABLE

class DispatchedUnit(BaseModel):
    incident_id: int
    unit_id: int
    dispatched_at: datetime
    returned_at: Optional[datetime] = None
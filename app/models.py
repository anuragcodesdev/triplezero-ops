from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional, Annotated


class IncidentStatus(str, Enum):
    reported = "reported"
    dispatched = "dispatched"
    contained = "contained"
    closed = "closed"


class Incidents(BaseModel):
    incident_type: str
    latitude: float
    longitude: float
    description: str
    severity: Annotated[int, Field(ge=1, le=4)]
    status: IncidentStatus
    reported_at: datetime
    closed_at: Optional[datetime] = None
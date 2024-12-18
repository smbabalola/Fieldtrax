# app/schemas/events.py
from enum import Enum
from pydantic import BaseModel
from typing import Any, Dict
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel,Field

class EventType(str, Enum):
    JOB_UPDATED = "job_updated"
    DAILY_REPORT_ADDED = "daily_report_added"
    FLUID_ADDED = "fluid_added"
    TALLY_UPDATED = "tally_updated"
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    ALERT = "alert"

class JobEvent(BaseModel):
    type: EventType
    job_id: UUID
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    data: Dict[str, Any]

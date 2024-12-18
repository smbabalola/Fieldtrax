# app/models/events.py
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any
from uuid import UUID

class EventType(str, Enum):
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    JOB_UPDATED = "job_updated"
    DAILY_REPORT_ADDED = "daily_report_added"
    FLUID_ADDED = "fluid_added"
    ALERT = "alert"
    ERROR = "error"

class JobEvent(BaseModel):
    type: EventType
    job_id: UUID
    user_id: str
    timestamp: datetime
    data: Dict[str, Any]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: str
        }
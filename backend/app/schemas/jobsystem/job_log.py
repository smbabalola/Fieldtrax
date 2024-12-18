#job_log
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class JobLogBase(TimeStampSchema):
    job_id: str
    timestamp: datetime
    activity_type: str
    description: Optional[str] = None
    duration: Optional[float] = None
    

class JobLogCreate(JobLogBase):
    job_id: str
    timestamp: datetime
    activity_type: str
    description: Optional[str] = None
    duration: Optional[float] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class JobLogUpdate(JobLogBase):
    pass

class JobLogResponse(JobLogBase):
    id: str

    class Config:
        from_attributes = True

class JobLogView(JobLogResponse):
    pass


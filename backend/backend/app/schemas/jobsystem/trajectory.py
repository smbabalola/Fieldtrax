#trajectory
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class TrajectoryBase(TimeStampSchema):
    wellbore_id: str
    measured_depth: float
    inclination: float
    azimuth: float
    

class TrajectoryCreate(TrajectoryBase):
    wellbore_id: str
    measured_depth: float
    inclination: float
    azimuth: float
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
        
class TrajectoryUpdate(TrajectoryBase):
    pass

class TrajectoryResponse(TrajectoryBase):
    id: str

    class Config:
        from_attributes = True

class TrajectoryView(TrajectoryResponse):
    pass
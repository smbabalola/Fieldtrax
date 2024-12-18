#rig

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class RigBase(TimeStampSchema):
    rig_name: str
    contractor_id: str
    air_gap: float
    rig_type_id: str
    water_depth: float
    

class RigCreate(RigBase):
    rig_name: str
    contractor_id: str
    air_gap: float
    rig_type_id: str
    water_depth: float
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
class RigUpdate(RigBase):
    pass

class RigResponse(RigBase):
    id: str

    class Config:
        from_attributes = True

class RigView(RigResponse):
    pass

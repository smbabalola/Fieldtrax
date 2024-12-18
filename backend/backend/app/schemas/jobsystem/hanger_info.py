#hanger_info
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class HangerInfoBase(TimeStampSchema):
    wellbore_id: Optional[str] = None
    type: Optional[str] = None
    burst_rating: Optional[float] = None
    tensile_rating: Optional[float] = None
    hanging_capacity: Optional[float] = None
    hydraulic_setting_pressure: Optional[float] = None
    
class HangerInfoCreate(HangerInfoBase):
    wellbore_id: Optional[str] = None
    type: Optional[str] = None
    burst_rating: Optional[float] = None
    tensile_rating: Optional[float] = None
    hanging_capacity: Optional[float] = None
    hydraulic_setting_pressure: Optional[float] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class HangerInfoUpdate(HangerInfoBase):
    pass

class HangerInfoResponse(HangerInfoBase):
    id: str

    class Config:
        from_attributes = True

class HangerInfoView(HangerInfoResponse):
    pass
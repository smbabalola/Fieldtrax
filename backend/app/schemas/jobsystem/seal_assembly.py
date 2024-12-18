
#seal_assembly
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class SealAssemblyBase(TimeStampSchema):
    wellbore_id: Optional[str] = None
    seal_surface_od: Optional[float] = None
    body_burst: Optional[float] = None
    collapse: Optional[float] = None
    tensile: Optional[float] = None
    tieback_extension_id: Optional[float] = None
    tieback_extension_burst: Optional[float] = None
    tieback_extension_collapse: Optional[float] = None
    tieback_yield_collapse: Optional[float] = None
    setting_force: Optional[float] = None
    hold_down_slips: Optional[bool] = None
    element_rating: Optional[float] = None
    slick_stinger_od: Optional[float] = None
    
class SealAssemblyCreate(SealAssemblyBase):
    wellbore_id: Optional[str] = None
    seal_surface_od: Optional[float] = None
    body_burst: Optional[float] = None
    collapse: Optional[float] = None
    tensile: Optional[float] = None
    tieback_extension_id: Optional[float] = None
    tieback_extension_burst: Optional[float] = None
    tieback_extension_collapse: Optional[float] = None
    tieback_yield_collapse: Optional[float] = None
    setting_force: Optional[float] = None
    hold_down_slips: Optional[bool] = None
    element_rating: Optional[float] = None
    slick_stinger_od: Optional[float] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class SealAssemblyUpdate(SealAssemblyBase):
    pass

class SealAssemblyResponse(SealAssemblyBase):
    id: str

    class Config:
        from_attributes = True

class SealAssemblyView(SealAssemblyResponse):
    pass


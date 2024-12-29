#fluid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class CMTJOBBase(TimeStampSchema):
    wellbore_id: str
    off_bottom_cement_type: Optional[str]
    open_hole_packer_depth: Optional[float]
    open_hole_packers: Optional[bool]
    screen_supplier: Optional[str]
    fluid_loss: Optional[bool]
    pac_valve_depth: Optional[float]
    packer_above_screens: Optional[bool]
    pressure_below_ECP: Optional[float]
    
    
class CMTJOBCreate(CMTJOBBase):
    wellbore_id: str
    off_bottom_cement_type: Optional[str]
    open_hole_packer_depth: Optional[float]
    open_hole_packers: Optional[bool]
    screen_supplier: Optional[str]
    fluid_loss: Optional[bool]
    pac_valve_depth: Optional[float]
    packer_above_screens: Optional[bool]
    pressure_below_ECP: Optional[float]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
        
class CMTJOBUpdate(CMTJOBBase):    
    pass

class CMTJOBResponse(CMTJOBBase):
    id: str
    
    class Config:
        from_attributes = True
        
class CMTJOBView(CMTJOBResponse):
    pass


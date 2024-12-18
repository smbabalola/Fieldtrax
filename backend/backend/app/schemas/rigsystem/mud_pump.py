#mud_pump
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class MudPumpBase(TimeStampSchema):
    rig_id: str
    serial_number: Optional[str] = None
    stroke_length: Optional[float] = None
    max_pressure: Optional[float] = None
    power_rating: Optional[float] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    efficiency: Optional[float] = None
    pump_type: Optional[str] = None
    

class MudPumpCreate(MudPumpBase):
    pass

class MudPumpUpdate(MudPumpBase):
    pass

class MudPumpResponse(MudPumpBase):
    id: str

    class Config:
        from_attributes = True

class MudPumpView(MudPumpResponse):  #
    pass  
    
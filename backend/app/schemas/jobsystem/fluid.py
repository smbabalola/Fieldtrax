#fluid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class FluidBase(TimeStampSchema):
    wellbore_id: str
    report_date: datetime
    sample_from: str
    fluid_type: str
    mud_weight: float
    funnel_viscosity: float
    plastic_viscosity: float
    yield_point: float
    gel_strength: float
    pH: float
    r600: float
    r300: float
    r200: float
    r100: float
    r6: float
    r3: float
    test_number: int
    
class FluidCreate(FluidBase):
    wellbore_id: str
    report_date: datetime
    sample_from: str
    fluid_type: str
    mud_weight: float
    funnel_viscosity: float
    plastic_viscosity: float
    yield_point: float
    gel_strength: float
    pH: float
    r600: float
    r300: float
    r200: float
    r100: float
    r6: float
    r3: float
    test_number: int
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class FluidUpdate(FluidBase):
    pass

class FluidResponse(FluidBase):
    id: str

    class Config:
        from_attributes = True

class FluidView(FluidResponse):
    pass

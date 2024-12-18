#fluid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class FluidBase(TimeStampSchema):
    wellbore_id: str
    fluid_type: str
    volume_value: float
    volume_unit: Optional[str] = None
    density_value: float
    density_unit: Optional[str] = None
    viscosity_value: Optional[float] = None
    viscosity_unit: Optional[str] = None
    description: Optional[str] = None
    # timestamp: Optional[datetime] = None

class FluidCreate(FluidBase):
    wellbore_id: str
    fluid_type: str
    volume_value: float
    volume_unit: Optional[str] = None
    density_value: float
    density_unit: Optional[str] = None
    viscosity_value: Optional[float] = None
    viscosity_unit: Optional[str] = None
    description: Optional[str] = None
    # timestamp: Optional[datetime] = None
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

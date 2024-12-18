#well_control_Equipment
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, condecimal, field_validator
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class WellBase(TimeStampSchema):
    
    slot_id: str = Field(..., max_length=50)
    well_name: str = Field(..., min_length=1, max_length=100)
    short_name: Optional[str] = Field(None, max_length=50)
    api_number: Optional[str] = Field(None, max_length=20)
    spud_date: Optional[datetime] = None
    well_type_id: Optional[str] = Field(None, max_length=50)
    production_id: Optional[str] = Field(None, max_length=50)
    well_shape_id: Optional[str] = Field(None, max_length=50)
    measured_depth: float = Field(default=0, ge=0)
    total_vertical_depth: float = Field(default=0, ge=0)
        


class WellCreate(WellBase):
    
    slot_id: str = Field(..., max_length=50)
    well_name: str = Field(..., min_length=1, max_length=100)
    short_name: Optional[str] = Field(None, max_length=50)
    api_number: Optional[str] = Field(None, max_length=20)
    spud_date: Optional[datetime] = None
    well_type_id: Optional[str] = Field(None, max_length=50)
    production_id: Optional[str] = Field(None, max_length=50)
    well_shape_id: Optional[str] = Field(None, max_length=50)
    measured_depth: float = Field(default=0, ge=0)
    total_vertical_depth: float = Field(default=0, ge=0)
        
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class WellUpdate(WellBase):
    slot_id: Optional[str] = Field(None, max_length=50)
    well_name: Optional[str] = Field(None, min_length=1, max_length=100)
    short_name: Optional[str] = Field(None, max_length=50)
    api_number: Optional[str] = Field(None, max_length=20)
    spud_date: Optional[datetime] = None
    well_type_id: Optional[str] = Field(None, max_length=50)
    production_id: Optional[str] = Field(None, max_length=50)
    well_shape_id: Optional[str] = Field(None, max_length=50)
    measured_depth: Optional[float] = Field(None, ge=0)
    total_vertical_depth: Optional[float] = Field(None, ge=0)

class WellResponse(WellBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class WellView(WellResponse):
    pass


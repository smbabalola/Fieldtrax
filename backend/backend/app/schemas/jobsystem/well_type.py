# File: backend/app/schemas/wellsystem/well_type.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class WellTypeBase(TimeStampSchema):
    well_type_name: str = Field(..., description="Name of the well type")
    description: Optional[str] = Field(None, description="Description of the well type")

class WellTypeCreate(WellTypeBase):
    well_type_name: str 
    description: Optional[str]

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class WellTypeUpdate(WellTypeBase):
    well_type_name: Optional[str]
    description: Optional[str]

class WellTypeResponse(WellTypeBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

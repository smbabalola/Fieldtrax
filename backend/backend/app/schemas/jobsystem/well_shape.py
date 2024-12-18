# File: backend/app/schemas/wellsystem/well_shape.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WellShapeBase(BaseModel):
    well_shape: str = Field(..., description="Name of the well shape")
    description: Optional[str] = Field(None, description="Description of the well shape")

class WellShapeCreate(WellShapeBase):
    well_shape: str 
    description: Optional[str]

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class WellShapeUpdate(WellShapeBase):
    # name: Optional[str] = Field(None, description="Name of the well shape")
    pass

class WellShapeResponse(WellShapeBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
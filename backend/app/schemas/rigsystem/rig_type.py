# File: backend/app/schemas/wellsystem/rig_type.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class RigTypeBase(TimeStampSchema):
    """Base schema for Rig Type"""
    rig_type_name: str = Field(..., 
                     description="Name of the rig type",
                     max_length=100)
    description: Optional[str] = Field(None, 
                                     description="Description of the rig type",
                                     max_length=500)

class RigTypeCreate(RigTypeBase):
    """Schema for creating a new Rig Type"""
    rig_type_name: str = Field(..., 
                     description="Name of the rig type",
                     max_length=100)
    description: Optional[str] = Field(None, 
                                     description="Description of the rig type",
                                     max_length=500)
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class RigTypeUpdate(BaseModel):
    """Schema for updating a Rig Type"""
    rig_type_name: Optional[str] = Field(None, 
                               description="Name of the rig type",
                               max_length=100)
    description: Optional[str] = Field(None, 
                                     description="Description of the rig type",
                                     max_length=500)

class RigTypeResponse(RigTypeBase):
    """Schema for Rig Type response"""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "RT001",
                "name": "Conventional",
                "description": "Traditional rotary drilling rig",
                "created_at": "2024-02-20T12:00:00Z",
                "updated_at": "2024-02-20T12:00:00Z"
            }
        }
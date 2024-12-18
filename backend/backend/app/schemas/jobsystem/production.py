#production
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class ProductionBase(TimeStampSchema):
    production_type: Optional[str] = None
    description: Optional[str] = None

class ProductionCreate(ProductionBase):
    production_type: Optional[str] = None
    description: Optional[str] = None    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class ProductionUpdate(ProductionBase):
    pass

class ProductionResponse(ProductionBase):
    id: str

    class Config:
        from_attributes = True

class ProductionView(ProductionResponse):
    pass
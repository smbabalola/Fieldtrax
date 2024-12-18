#tubularType
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class TubularTypeBase(TimeStampSchema):
    type: Optional[str] = None
    type_short: Optional[str] = None
    description: Optional[str] = None

class TubularTypeCreate(TubularTypeBase):
    type: Optional[str] = None
    type_short: Optional[str] = None
    description: Optional[str] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class TubularTypeUpdate(TubularTypeBase):
    pass

class TubularTypeResponse(TubularTypeBase):
    id: str

    class Config:
        from_attributes = True

class TubularTypeView(TubularTypeResponse):
    pass
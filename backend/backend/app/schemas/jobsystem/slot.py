#slot
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class SlotBase(TimeStampSchema):
    installation_id: Optional[str] = None
    slot_name: Optional[str] = None
    utm_eastings: Optional[float] = None
    utm_northings: Optional[float] = None
    longitude: Optional[str] = None
    latitude: Optional[str] = None

class SlotCreate(SlotBase):
    installation_id: Optional[str] = None
    slot_name: Optional[str] = None
    utm_eastings: Optional[float] = None
    utm_northings: Optional[float] = None
    longitude: Optional[str] = None
    latitude: Optional[str] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class SlotUpdate(SlotBase):
    pass

class SlotResponse(SlotBase):
    id: str

    class Config:
        from_attributes = True

class SlotView(SlotResponse):
    pass

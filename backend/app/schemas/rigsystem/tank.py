#tank
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class TankBase(TimeStampSchema):
    rig_id: int
    tank_name: Optional[str] = None
    capacity: Optional[float] = None
    shape: Optional[str] = None
    length: Optional[float] = None
    height: Optional[float] = None
    width_top: Optional[float] = None
    width_bottom: Optional[float] = None

class TankCreate(TankBase):
    rig_id: int
    tank_name: Optional[str] = None
    capacity: Optional[float] = None
    shape: Optional[str] = None
    length: Optional[float] = None
    height: Optional[float] = None
    width_top: Optional[float] = None
    width_bottom: Optional[float] = None

class TankUpdate(TankBase):
    pass

class TankResponse(TankBase):
    id: str

    class Config:
        from_attributes = True

class TankView(TankResponse):
    pass

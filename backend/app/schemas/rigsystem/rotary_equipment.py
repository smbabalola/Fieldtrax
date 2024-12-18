#rotary_equipment
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class RotaryEquipmentBase(TimeStampSchema):
    rig_id: str
    top_drive_manufacturer: Optional[str] = None
    top_drive_model: Optional[str] = None
    top_drive_power_rating: Optional[float] = None
    top_drive_torque_rating: Optional[float] = None
    top_drive_weight: Optional[float] = None
    rotary_table_manufacturer: Optional[str] = None
    rotary_table_model: Optional[str] = None
    rotary_table_power_rating: Optional[float] = None
    rotary_table_torque_rating: Optional[float] = None

class RotaryEquipmentCreate(RotaryEquipmentBase):
    rig_id: str
    top_drive_manufacturer: Optional[str] = None
    top_drive_model: Optional[str] = None
    top_drive_power_rating: Optional[float] = None
    top_drive_torque_rating: Optional[float] = None
    top_drive_weight: Optional[float] = None
    rotary_table_manufacturer: Optional[str] = None
    rotary_table_model: Optional[str] = None
    rotary_table_power_rating: Optional[float] = None
    rotary_table_torque_rating: Optional[float] = None

class RotaryEquipmentUpdate(RotaryEquipmentBase):
    pass

class RotaryEquipmentResponse(RotaryEquipmentBase):
    id: str

    class Config:
        from_attributes = True

class RotaryEquipmentView(RotaryEquipmentResponse):
    pass
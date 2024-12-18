#rig_equipment
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class RigEquipmentBase(TimeStampSchema):
    rig_id: str
    derrick_height: Optional[float] = None
    derrick_rating: Optional[float] = None
    derrick_manufacturer: Optional[str] = None
    rig_model: Optional[str] = None
    rig_power: Optional[float] = None
    travel_equipment_weight: Optional[float] = None
    kelly_manufacturer: Optional[str] = None
    kelly_type: Optional[str] = None
    kelly_length: Optional[float] = None
    kelly_weight: Optional[float] = None
    kelly_internal_diameter: Optional[float] = None
    surface_pipe_one_id: Optional[float] = None
    surface_pipe_one_length: Optional[float] = None
    surface_pipe_one_pressure_rating: Optional[float] = None
    surface_pipe_two_id: Optional[float] = None
    surface_pipe_two_length: Optional[float] = None
    surface_pipe_two_pressure_rating: Optional[float] = None
    stand_pipe_id: Optional[float] = None
    stand_pipe_length: Optional[float] = None
    stand_pipe_pressure_rating: Optional[float] = None
    kelly_hose_id: Optional[float] = None
    kelly_hose_length: Optional[float] = None
    kelly_hose_pressure_rating: Optional[float] = None


class RigEquipmentCreate(RigEquipmentBase):
    pass

class RigEquipmentUpdate(RigEquipmentBase):
    pass

class RigEquipmentResponse(RigEquipmentBase):
    id: str

    class Config:
        from_attributes = True

class RigEquipmentView(RigEquipmentResponse):
    pass
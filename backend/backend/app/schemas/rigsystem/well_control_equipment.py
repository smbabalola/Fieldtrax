from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class WellControlEquipmentBase(TimeStampSchema):
    rig_id: str
    choke_line_diameter: Optional[float] = None
    choke_line_pressure: Optional[float] = None
    kill_line_diameter: Optional[float] = None
    bop_size: Optional[float] = None
    bop_max_pressure: Optional[float] = None
    bop_max_temperature: Optional[float] = None
    diverter_manufacturer: Optional[str] = None
    diverter_model: Optional[str] = None
    line_number: Optional[int] = None
    internal_diameter: Optional[float] = None
    max_pressure: Optional[float] = None
    line_length: Optional[float] = None
    closing_time: Optional[float] = None
    
class WellControlEquipmentCreate(WellControlEquipmentBase):
    rig_id: str
    choke_line_diameter: Optional[float] = None
    choke_line_pressure: Optional[float] = None
    kill_line_diameter: Optional[float] = None
    bop_size: Optional[float] = None
    bop_max_pressure: Optional[float] = None
    bop_max_temperature: Optional[float] = None
    diverter_manufacturer: Optional[str] = None
    diverter_model: Optional[str] = None
    line_number: Optional[int] = None
    internal_diameter: Optional[float] = None
    max_pressure: Optional[float] = None
    line_length: Optional[float] = None
    closing_time: Optional[float] = None

class WellControlEquipmentUpdate(WellControlEquipmentBase):
    pass

class WellControlEquipmentResponse(WellControlEquipmentBase):
    id: str

    class Config:
        from_attributes = True

class WellControlEquipmentView(WellControlEquipmentResponse):
    pass

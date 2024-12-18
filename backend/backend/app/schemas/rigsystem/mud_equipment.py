from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

# mud_equipment
class MudEquipmentBase(TimeStampSchema):
    rig_id: str
    equipment_name: Optional[str] = None
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None


class MudEquipmentCreate(MudEquipmentBase):
    pass

class MudEquipmentUpdate(MudEquipmentBase):
    pass

class MudEquipmentResponse(MudEquipmentBase):
    id: str

    class Config:
        from_attributes = True

class MudEquipmentView(MudEquipmentResponse):
    pass

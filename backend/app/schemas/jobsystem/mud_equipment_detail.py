from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

#mud_equipment_detail
class MudEquipmentDetailBase(TimeStampSchema):
    report_id: str
    mud_equipment_id: int
    hours_run: Optional[int] = None
    screen_sizes: Optional[str] = None
    active_volume_lost: Optional[float] = None
    reserve_volume_lost: Optional[float] = None
    other: Optional[float] = None

class MudEquipmentDetailCreate(MudEquipmentDetailBase):
    report_id: str
    mud_equipment_id: int
    hours_run: Optional[int] = None
    screen_sizes: Optional[str] = None
    active_volume_lost: Optional[float] = None
    reserve_volume_lost: Optional[float] = None
    other: Optional[float] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class MudEquipmentDetailUpdate(MudEquipmentDetailBase):
    pass

class MudEquipmentDetailResponse(MudEquipmentDetailBase):
    id: str

    class Config:
        from_attributes = True

class MudEquipmentDetailView(MudEquipmentDetailResponse):
    pass

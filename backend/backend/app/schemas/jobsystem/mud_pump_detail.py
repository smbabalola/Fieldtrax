#mud_pump_detail
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class MudPumpDetailBase(TimeStampSchema):
    report_id: str
    mud_pump_id: int
    circulation_rate: float
    for_hole: bool

class MudPumpDetailCreate(MudPumpDetailBase):
    report_id: str
    mud_pump_id: int
    circulation_rate: float
    for_hole: bool
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class MudPumpDetailUpdate(MudPumpDetailBase):
    pass

class MudPumpDetailResponse(MudPumpDetailBase):
    id: str

    class Config:
        from_attributes = True

class MudPumpDetailView(MudPumpDetailResponse):
    pass
#tally_item#
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class TallyItemBase(TimeStampSchema):
    tally_id: str
    length_value: float
    length_unit: Optional[str] = None
    outer_diameter_value: float
    outer_diameter_unit: Optional[str] = None
    inner_diameter_value: Optional[float] = None
    inner_diameter_unit: Optional[str] = None
    weight_per_unit_value: float
    weight_per_unit_unit: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None

class TallyItemCreate(TallyItemBase):
    tally_id: str
    length_value: float
    length_unit: Optional[str] = None
    outer_diameter_value: float
    outer_diameter_unit: Optional[str] = None
    inner_diameter_value: Optional[float] = None
    inner_diameter_unit: Optional[str] = None
    weight_per_unit_value: float
    weight_per_unit_unit: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class TallyItemUpdate(TallyItemBase):
    pass

class TallyItemResponse(TallyItemBase):
    id: str

    class Config:
        from_attributes = True

class TallyItewmView(TallyItemBase):
    pass
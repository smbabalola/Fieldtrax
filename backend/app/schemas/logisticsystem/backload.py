from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class BackloadBase(TimeStampSchema):
    wellbore_id: str
    sheet_number: str
    date: datetime
    destination: str
    total_weight_value: float
    total_weight_unit: Optional[str] = None
    transportation_details: Optional[str] = None
    status: Optional[str] = None
    approved_by: Optional[str] = None

class BackloadCreate(BackloadBase):
    pass

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class BackloadUpdate(BackloadBase):
    wellbore_id: str
    sheet_number: str
    date: datetime
    destination: str
    total_weight_value: float
    total_weight_unit: Optional[str] = None
    transportation_details: Optional[str] = None
    status: Optional[str] = None
    approved_by: Optional[str] = None

class BackloadResponse(BackloadBase):
    id: str

    class Config:
        from_attributes = True

class BackloadView(BackloadResponse):
    pass

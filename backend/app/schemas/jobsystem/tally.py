#tally
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class TallyBase(TimeStampSchema):
    wellbore_id: str
    tally_type: str
    date: datetime
    total_length_value: float
    total_length_unit: Optional[str] = None
    total_weight_value: float
    total_weight_unit: Optional[str] = None
    created_by: str
    verified_by: Optional[str] = None

class TallyCreate(TallyBase):
    wellbore_id: str
    tally_type: str
    date: datetime
    total_length_value: float
    total_length_unit: Optional[str] = None
    total_weight_value: float
    total_weight_unit: Optional[str] = None
    created_by: str
    verified_by: Optional[str] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class TallyUpdate(TallyBase):
    pass

class TallyResponse(TallyBase):
    id: str

    class Config:
        from_attributes = True

class TallyView(TallyResponse):
    pass
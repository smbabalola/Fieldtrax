#time_sheet
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class TimeSheetBase(TimeStampSchema):
    wellbore_id: str
    job_id: str
    employee_id: str
    date: datetime
    hours_worked: float
    activity_code: str
    description: Optional[str] = None
    approved: Optional[bool] = None
    approved_by: Optional[str] = None
    approval_date: Optional[datetime] = None

class TimeSheetCreate(TimeSheetBase):
    wellbore_id: str
    job_id: str
    employee_id: str
    date: datetime
    hours_worked: float
    activity_code: str
    description: Optional[str] = None
    approved: Optional[bool] = None
    approved_by: Optional[str] = None
    approval_date: Optional[datetime] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
class TimeSheetUpdate(TimeSheetBase):
    pass

class TimeSheetResponse(TimeSheetBase):
    id: str

    class Config:
        from_attributes = True

class TimeSheetView(TimeSheetResponse):
    pass
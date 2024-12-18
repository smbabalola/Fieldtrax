# #daily_report.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class DailyReportBase(TimeStampSchema):
    wellbore_id: str
    report_date: datetime
    # created_at: Optional[datetime] = None
    # updated_at: Optional[datetime] = None

class DailyReportCreate(DailyReportBase):
    wellbore_id: str
    report_date: datetime
    # created_at: Optional[datetime] = None
    # updated_at: Optional[datetime] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class DailyReportUpdate(DailyReportBase):
    pass

class DailyReportResponse(DailyReportBase):
    id: str

    class Config:
        from_attributes = True

class DailyReportView(DailyReportResponse):
    pass
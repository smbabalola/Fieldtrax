from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema


#job_center
class JobCenterBase(TimeStampSchema):
    # slot_id: int
    well_name: str
    short_name: Optional[str] = None
    api_number: Optional[str] = None
    description: Optional[str] = None
    # spud_date: Optional[datetime] = None
    # well_class_id: int
    # production_id: int
    # well_shape_id: int
    # utm_eastings: Optional[float] = None
    # utm_northings: Optional[float] = None
    # latitude: Optional[str] = None
    # longitude: Optional[str] = None
    # water_depth: Optional[float] = None
    # district: Optional[str] = None
    # address_1: Optional[str] = None
    # address_2: Optional[str] = None
    # post_code: Optional[str] = None
    # county: Optional[str] = None
    # country: Optional[str] = None
    # updated_by: Optional[int] = None
    # date_last_updated: Optional[datetime] = None

class JobCenterCreate(JobCenterBase):
    well_name: str
    short_name: Optional[str] = None
    api_number: Optional[str] = None
    description: Optional[str] = None


    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
class JobCenterUpdate(JobCenterBase):
    well_name: str
    short_name: Optional[str] = None
    api_number: Optional[str] = None
    description: Optional[str] = None

class JobCenterResponse(JobCenterBase):
    id: str

    class Config:
        from_attributes = True

class JobCenterView(JobCenterResponse):
    pass

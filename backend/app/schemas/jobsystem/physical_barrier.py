#physical_barrier
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class PhysicalBarrierBase(TimeStampSchema):
    wellbore_id: str
    job_id: str
    barrier_type: str
    depth_value: float
    depth_unit: Optional[str] = None
    length_value: Optional[float] = None
    length_unit: Optional[str] = None
    pressure_rating_value: float
    pressure_rating_unit: Optional[str] = None
    installation_date: datetime
    installed_by: str
    verified_by: Optional[str] = None
    verification_date: Optional[datetime] = None

class PhysicalBarrierCreate(PhysicalBarrierBase):
    wellbore_id: str
    job_id: str
    barrier_type: str
    depth_value: float
    depth_unit: Optional[str] = None
    length_value: Optional[float] = None
    length_unit: Optional[str] = None
    pressure_rating_value: float
    pressure_rating_unit: Optional[str] = None
    installation_date: datetime
    installed_by: str
    verified_by: Optional[str] = None
    verification_date: Optional[datetime] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }


class PhysicalBarrierUpdate(PhysicalBarrierBase):
    pass

class PhysicalBarrierResponse(PhysicalBarrierBase):
    id: str

    class Config:
        from_attributes = True

class PhysicalBarrierView(PhysicalBarrierResponse):
    pass
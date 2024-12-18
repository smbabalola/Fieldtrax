        
#wellbore
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class WellboreBase(TimeStampSchema):
    job_id: str
    well_id: str
    short_name: str
    wellbore_name: str
    description: Optional[str] = None
    wellbore_number: Optional[str] = None
    # contract_type_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    primary_currency: Optional[str] = None
    secondary_currency: Optional[str] = None
    planned_start_date: Optional[datetime] = None
    Planned_days: Optional[int] = None
    Planned_well_cost: Optional[float] = None
    actual_well_cost: Optional[float] = None

class WellboreCreate(WellboreBase):
    job_id: str
    well_id: str
    short_name: str
    wellbore_name: str
    description: Optional[str] = None
    wellbore_number: Optional[str] = None
    # contract_type_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    primary_currency: Optional[str] = None
    secondary_currency: Optional[str] = None
    planned_start_date: Optional[datetime] = None
    Planned_days: Optional[int] = None
    Planned_well_cost: Optional[float] = None
    actual_well_cost: Optional[float] = None
    
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
    
class WellboreUpdate(WellboreBase):
    pass

class WellboreResponse(WellboreBase):
    id: str

    class Config:
        from_attributes = True

class WellboreView(WellboreResponse):
    pass
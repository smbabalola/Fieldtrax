from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from sqlalchemy import DateTime

from app.models.base import TimeStampSchema

class ActivityBase(TimeStampSchema):
    
    job_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow) 
    type: str
    description: str
    user_id: str
    
class ActivityCreate(ActivityBase):
    job_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow) 
    type: str
    description: str
    user_id: str
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class ActivityUpdate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: str

    class Config:
        from_attributes = True

class ContractTypeView(ActivityResponse):
    pass
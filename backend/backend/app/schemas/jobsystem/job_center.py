from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class JobCenterBase(BaseModel):
    job_center_name:str
    description:str

class JobCenterCreate(JobCenterBase):
    job_center_name: str
    description: str
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class JobCenterUpdate(JobCenterBase):
    job_center_name: str
    description: str

class JobCenterResponse(JobCenterBase):
    id: str

    class Config:
        from_attributes = True

class JobCenterView(JobCenterResponse):
    pass
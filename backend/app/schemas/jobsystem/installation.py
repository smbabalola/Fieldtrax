#installation
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class InstallationBase(TimeStampSchema):
    field_id: Optional[str] = None
    installation_name: Optional[str] = None
    installation_type_id: Optional[str] = None
    field_block: Optional[str] = None
    water_depth: Optional[float] = None
	# [updated_by] [int] NOT NULL,
    # date_last_updated: Optional[datetime] = None
    

class InstallationCreate(InstallationBase):
    field_id: Optional[str] = None
    installation_name: Optional[str] = None
    installation_type_id: Optional[str] = None
    field_block: Optional[str] = None
    water_depth: Optional[float] = None
	# [updated_by] [int] NOT NULL,
    # date_last_updated: Optional[datetime] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class InstallationUpdate(InstallationBase):
    pass

class InstallationResponse(InstallationBase):
    id: str

    class Config:
        from_attributes = True

class InstallationView(InstallationResponse):
    pass

    
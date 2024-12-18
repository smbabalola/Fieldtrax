#installationType
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class InstallationTypeBase(TimeStampSchema):
    installation_type: Optional[str] = None
    # name: Optional[str] = None
    description: Optional[str] = None
    
class InstallationTypeResponse(InstallationTypeBase):

    class Config:
        from_attributes = True
        
class InstallationTypeUpdateDetails(InstallationTypeBase):

    class Config:
        from_attributes = True
        
class InstallationTypeCreate(InstallationTypeBase):
    installation_type: Optional[str] = None
    # name: Optional[str] = None
    description: Optional[str] = None    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class InstallationTypeUpdate(InstallationTypeBase):
    pass

class InstallationTypeResponse(InstallationTypeBase):
    id: str

    class Config:
        from_attributes = True

class InstallationTypeView(InstallationTypeResponse):
    pass


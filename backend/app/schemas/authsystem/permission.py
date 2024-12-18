from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    resource: str
    action: str

    class Config:
        from_attributes = True

class PermissionCreate(PermissionBase):
    name: str
    description: Optional[str] = None
    resource: str
    action: str
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class PermissionUpdate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: int

    class Config:
        from_attributes = True

class PermissionView(PermissionResponse):
    role = str
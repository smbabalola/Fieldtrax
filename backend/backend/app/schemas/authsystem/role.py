from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class RoleCreate(RoleBase):
    name: str
    description: Optional[str] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class RoleUpdate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True

class RoleView(RoleResponse):
    permissions: List[str] = []
    users: List[str] = []
    
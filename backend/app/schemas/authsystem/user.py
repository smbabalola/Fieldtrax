# File: app/schemas/authsystem/user.py
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from app.models.base import TimeStampSchema
from .role import RoleResponse

class UserBase(TimeStampSchema):
    email: EmailStr = Field(..., max_length=50)
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=50)
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def password_complexity(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, max_length=50)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    verification_token: Optional[str] = Field(None, max_length=500)

class UserResponse(UserBase):
    id: str
    is_active: bool
    is_verified: bool

class UserView(UserResponse):
    roles: List[RoleResponse] = []
    active_sessions_count: int = 0

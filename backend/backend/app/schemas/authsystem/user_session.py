# File: backend/app/schemas/authsystem/user_session.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import datetime

from app.models.base import TimeStampSchema

class UserSessionBase(TimeStampSchema):
    user_id: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: datetime
    created_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    is_active: Optional[bool] = None
    device_info: Optional[str] = None
    ip_address: Optional[str] = None

class UserSessionCreate(UserSessionBase):
    user_id: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: datetime
    created_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    is_active: Optional[bool] = None
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class UserSessionUpdate(UserSessionBase):
    pass

class UserSessionResponse(UserSessionBase):
    id: str

    class Config:
        from_attributes = True

class UserSessionView(UserSessionResponse):
    class Config:
        from_attributes = True

# Optional enhanced schemas that can be used alongside the base ones
class DeviceInfo(BaseModel):
    """Optional enhanced device info"""
    device_type: Optional[str] = None
    os: Optional[str] = None
    browser: Optional[str] = None
    is_mobile: Optional[bool] = None
    is_tablet: Optional[bool] = None
    is_pc: Optional[bool] = None

    def to_str(self) -> str:
        """Convert to string format for compatibility with base schema"""
        return f"{self.device_type}|{self.os}|{self.browser}"

    @classmethod
    def from_str(cls, device_info: str) -> "DeviceInfo":
        """Create from string format for compatibility with base schema"""
        if not device_info:
            return cls()
        try:
            device_type, os, browser = device_info.split("|")
            return cls(
                device_type=device_type,
                os=os,
                browser=browser
            )
        except:
            return cls()

class SessionStatus(BaseModel):
    """Optional session status tracking"""
    is_valid: bool
    requires_verification: bool = False
    suspicious_activity: bool = False
    verification_reason: Optional[str] = None

class SessionAnalytics(BaseModel):
    """Optional session analytics"""
    login_count: int = 1
    last_locations: list[str] = []
    known_devices: list[str] = []
    suspicious_attempts: int = 0
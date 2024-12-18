from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

#password_reset
class PasswordResetBase(TimeStampSchema):
    user_id: str
    token: str
    is_used: Optional[bool] = None
    # created_at: Optional[datetime] = None
    # expires_at: datetime

class PasswordResetCreate(PasswordResetBase):
    user_id: str
    token: str
    is_used: Optional[bool] = None
    # created_at: Optional[datetime] = None
    # expires_at: datetime
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class PasswordResetUpdate(PasswordResetBase):
    pass

class PasswordResetResponse(PasswordResetBase):
    id: str

    class Config:
        from_attributes = True

class PasswordResetView(PasswordResetResponse):
    pass

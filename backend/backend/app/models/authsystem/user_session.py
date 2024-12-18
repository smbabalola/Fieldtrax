# File: backend/app/models/authsystem/user_session.py
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.utils import generate_uuid, utcnow
from app.database import Base
# import uuid
from datetime import datetime, timezone
from app.models.base import BaseDBModel
# from app.models.authsystem.user import User

# from app.models.authsystem.user import User

# def generate_uuid():
#     return str(uuid.uuid4())

# def utcnow():
#     return datetime.now(timezone.utc)

class UserSession(BaseDBModel):
    __tablename__ = 'user_session'

    # id = Column(String(50), primary_key=True, default=generate_uuid)
    user_id = Column(String(50), ForeignKey('users.id'), nullable=False)
    
    # Token information
    access_token = Column(String(500), nullable=False)  # Increased length for JWT
    refresh_token = Column(String(500), nullable=True)  # Increased length for JWT
    token_type = Column(String(20), default="bearer", nullable=False)
    
    # Timestamps
    expires_at = Column(DateTime, nullable=False)
    # created_at = Column(DateTime, default=utcnow, nullable=False)
    last_activity = Column(DateTime, nullable=True)
    revoked_at = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    revocation_reason = Column(String(100), nullable=True)
    
    # Device information
    device_info = Column(JSON, nullable=True)  # Stores detailed device info as JSON
    device_id = Column(String(64), nullable=True)  # Unique device identifier
    device_trusted = Column(Boolean, default=False, nullable=False)
    
    # Location information
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    location = Column(JSON, nullable=True)  # Stores geolocation data
    
    # Security flags
    suspicious_activity = Column(Boolean, default=False, nullable=False)
    requires_verification = Column(Boolean, default=False, nullable=False)
    
    # Relationship
    user = relationship('User', back_populates='user_sessions')

    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, active={self.is_active})>"

    @property
    def is_valid(self):
        """Check if session is valid"""
        return (
            self.is_active and
            not self.revoked and
            datetime.now(timezone.utc) < self.expires_at and
            not self.suspicious_activity
        )

    @property
    def device_info_dict(self):
        """Return device info as dictionary"""
        return self.device_info or {}

    @property
    def location_info_dict(self):
        """Return location info as dictionary"""
        return self.location or {}



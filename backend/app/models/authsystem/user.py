# File: app/models/authsystem/user.py
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseDBModel
from app.models.authsystem.associations import user_roles_table

class User(BaseDBModel):
    __tablename__ = 'users'

    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    full_name = Column(String(50), nullable=True)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(500), nullable=True)

    # Relationships
    password_resets = relationship('PasswordReset', back_populates='user')
    user_sessions = relationship('UserSession', back_populates='user')
    roles = relationship('Role', secondary=user_roles_table, back_populates='users')
    # user = relationship("User", back_populates="settings")
    settings = relationship("UserSetting", back_populates="user")
    activities = relationship("Activity", back_populates="user")

    def __repr__(self):
        return f"<User: {self.username}>"
# app/models/authsystem/password_reset.py
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseDBModel

class PasswordReset(BaseDBModel):
    __tablename__ = 'password_resets'

    user_id = Column(String(50), ForeignKey('users.id'), nullable=False)
    token = Column(String(500), unique=True, nullable=False)
    is_used = Column(Boolean, nullable=True, default=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='password_resets')

    def __repr__(self):
        return f"<PasswordReset: {self.id}>"
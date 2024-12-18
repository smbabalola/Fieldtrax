# app/models/base.py
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declared_attr
from pydantic import BaseModel as PydanticBaseModel
from app.database import Base  # Keep your existing import
import uuid

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class BaseDBModel(Base):
    """Base class for all SQLAlchemy models"""
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(String(50), primary_key=True, default=generate_uuid)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

class BaseSchema(PydanticBaseModel):
    """Base class for all Pydantic models"""
    class Config:
        from_attributes = True
        arbitrary_types_allowed=True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            uuid.UUID: str
        }

class TimeStampSchema(BaseSchema):
    """Mixin for models that need timestamp fields"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# For compatibility with existing code
BaseModel = BaseDBModel  # This maintains backward compatibility
from pydantic import BaseModel, ConfigDict
from typing import Optional, TypeVar, Generic, List
from datetime import datetime

class BaseSchema(BaseModel):
    """Base schema with common configurations"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

class TimestampSchema(BaseModel):
    """Schema mixin for timestamp fields"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class IDSchema(BaseSchema):
    """Schema mixin for ID field"""
    id: str

# Generic types for pagination
T = TypeVar('T')

class PaginatedResponse(BaseSchema, Generic[T]):
    """Generic paginated response schema"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

class MessageResponse(BaseSchema):
    """Standard message response schema"""
    message: str
    success: bool = True

class ErrorResponse(BaseSchema):
    """Standard error response schema"""
    error: str
    detail: Optional[str] = None
    status_code: int = 400
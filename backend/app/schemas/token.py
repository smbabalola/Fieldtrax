# app/schemas/token.py
from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    """Schema for access token response"""
    access_token: str
    token_type: str = "bearer"
    
class TokenPayload(BaseModel):
    """Schema for JWT token payload"""
    sub: Optional[str] = None
    exp: Optional[float] = None

class TokenCreate(BaseModel):
    """Schema for creating tokens (e.g., password reset)"""
    email: str

class TokenVerify(BaseModel):
    """Schema for verifying tokens"""
    token: str
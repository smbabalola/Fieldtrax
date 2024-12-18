# File: app/schemas/authsystem/user_roles.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class RoleAssignment(BaseModel):
    """Schema for assigning roles to a user"""
    role_ids: List[int]

class RoleAssignmentResponse(BaseModel):
    """Response schema for role assignment operations"""
    success: bool
    message: str
    assigned_roles: List[int] = []
    failed_roles: List[int] = []
    model_config = ConfigDict(from_attributes=True)

class UserRolesResponse(BaseModel):
    """Response schema for getting user's roles"""
    user_id: int
    roles: List[str]  # List of role names
    model_config = ConfigDict(from_attributes=True)
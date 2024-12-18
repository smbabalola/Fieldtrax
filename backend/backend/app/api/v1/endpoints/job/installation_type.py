# File: backend/app/api/v1/endpoints/installation/installation_type.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.jobsystem.installation_type import crud_installation_type
from app.schemas.jobsystem.installation_type import (
    InstallationTypeResponse as InstallationType, 
    InstallationTypeCreate, 
    InstallationTypeUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=InstallationType)
async def create_installation_type(
    type_in: InstallationTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new installation type"""
    return await crud_installation_type.create(db=db, obj_in=type_in)

@router.get("/type/{installation_type}", response_model=InstallationType)
async def get_installation_type(
    installation_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get installation type by name"""
    type_obj = await crud_installation_type.get_by_type(
        db=db,
        installation_type=installation_type
    )
    if not type_obj:
        raise HTTPException(status_code=404, detail="Installation type not found")
    return type_obj

@router.put("/{type_id}", response_model=InstallationType)
async def update_installation_type(
    type_id: str,
    type_in: InstallationTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update installation type"""
    type_obj = await crud_installation_type.get(db=db, id=type_id)
    if not type_obj:
        raise HTTPException(status_code=404, detail="Installation type not found")
    return await crud_installation_type.update(db=db, db_obj=type_obj, obj_in=type_in)



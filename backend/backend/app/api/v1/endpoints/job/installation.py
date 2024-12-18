
# File: backend/app/api/v1/endpoints/installation/installation.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.installation import crud_installation
from app.schemas.jobsystem.installation import (
    InstallationResponse as Installation, InstallationCreate, InstallationUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=Installation)
async def create_installation(
    installation_in: InstallationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new installation"""
    return await crud_installation.create(db=db, obj_in=installation_in)

@router.get("/field/{field_id}", response_model=List[Installation])
async def get_installations_by_field(
    field_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all installations in a field"""
    return await crud_installation.get_by_field(db=db, field_id=field_id)

@router.get("/name/{installation_name}", response_model=Installation)
async def get_installation_by_name(
    installation_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get installation by name"""
    installation = await crud_installation.get_by_name(db=db, installation_name=installation_name)
    if not installation:
        raise HTTPException(status_code=404, detail="Installation not found")
    return installation

@router.get("/type/{type_id}", response_model=List[Installation])
async def get_installations_by_type(
    type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get installations by type"""
    return await crud_installation.get_by_type(db=db, installation_type_id=type_id)

@router.put("/{installation_id}", response_model=Installation)
async def update_installation(
    installation_id: str,
    installation_in: InstallationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update installation"""
    installation = await crud_installation.get(db=db, id=installation_id)
    if not installation:
        raise HTTPException(status_code=404, detail="Installation not found")
    return await crud_installation.update(db=db, db_obj=installation, obj_in=installation_in)

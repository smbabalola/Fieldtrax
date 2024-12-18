# File: backend/app/api/v1/endpoints/well/well_type.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.well_type import crud_well_type
from app.schemas.jobsystem.well_type import (
    WellTypeResponse as WellType,
    WellTypeCreate,
    WellTypeUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()


@router.post("/", response_model=WellType)
async def create_well_type(
    well_type_in: WellTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new well type"""
    print(f"Received data: {well_type_in.dict()}")  # Add this line
    return await crud_well_type.create(db=db, obj_in=well_type_in)

@router.get("/type/{well_type}", response_model=WellType)
async def get_well_type(
    well_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get well type by name"""
    well = await crud_well_type.get_by_type(db=db, type_value=well_type, type_field="well_type_name")
    if not well:
        raise HTTPException(status_code=404, detail="Well type not found")
    return well

@router.put("/{type_id}", response_model=WellType)
async def update_well_type(
    type_id: str,
    well_type_in: WellTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update well type"""
    well_type = await crud_well_type.get(db=db, id=type_id)
    if not well_type:
        raise HTTPException(status_code=404, detail="Well type not found")
    return await crud_well_type.update(db=db, db_obj=well_type, obj_in=well_type_in)

@router.get("/", response_model=List[WellType])
async def get_all_well_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get all well types"""
    return await crud_well_type.get_all(db=db)

@router.delete("/{type_id}", response_model=dict)
async def delete_well_type(
    type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete well type"""
    well_type = await crud_well_type.get(db=db, id=type_id)
    if not well_type:
        raise HTTPException(status_code=404, detail="Well type not found")
    await crud_well_type.delete(db=db, id=type_id)
    return {"message": "Well type deleted successfully"}

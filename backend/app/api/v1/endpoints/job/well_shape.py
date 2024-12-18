# File: backend/app/api/v1/endpoints/well/well_shape.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.well_shape import crud_well_shape
from app.schemas.jobsystem.well_shape import (
    WellShapeResponse as WellShape,
    WellShapeCreate,
    WellShapeUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=WellShape)
async def create_well_shape(
    well_shape_in: WellShapeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new well shape"""
    return await crud_well_shape.create(db=db, obj_in=well_shape_in)

@router.get("/type/{well_shape}", response_model=WellShape)
async def get_well_shape(
    well_shape: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get well shape by name"""
    shape = await crud_well_shape.get_by_type(db=db, type_value=well_shape, type_field="well_shape")
    if not shape:
        raise HTTPException(status_code=404, detail="Well shape not found")
    return shape

@router.put("/{type_id}", response_model=WellShape)
async def update_well_shape(
    type_id: str,
    well_shape_in: WellShapeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update well shape"""
    well_shape = await crud_well_shape.get(db=db, id=type_id)
    if not well_shape:
        raise HTTPException(status_code=404, detail="Well shape not found")
    return await crud_well_shape.update(db=db, db_obj=well_shape, obj_in=well_shape_in)

@router.get("/", response_model=List[WellShape])
async def get_all_well_shapes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all well shapes"""
    return await crud_well_shape.get_all(db=db)

@router.delete("/{type_id}", response_model=dict)
async def delete_well_shape(
    type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete well shape"""
    well_shape = await crud_well_shape.get(db=db, id=type_id)
    if not well_shape:
        raise HTTPException(status_code=404, detail="Well shape not found")
    await crud_well_shape.delete(db=db, id=type_id)
    return {"message": "Well shape deleted successfully"}
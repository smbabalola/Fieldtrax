# File: backend/app/api/v1/endpoints/field/field.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.field import crud_field
from app.schemas.jobsystem.field import FieldResponse as Field, FieldCreate, FieldUpdate
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=Field)
async def create_field(
    field_in: FieldCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new field"""
    return await crud_field.create(db=db, obj_in=field_in)

@router.get("/name/{field_name}", response_model=Field)
async def get_field_by_name(
    field_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get field by name"""
    field = await crud_field.get_by_name(db=db, field_name=field_name)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    return field

@router.get("/country/{country}", response_model=List[Field])
async def get_fields_by_country(
    country: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all fields in a country"""
    return await crud_field.get_fields_by_country(db=db, country=country)

@router.get("/area/{area}", response_model=List[Field])
async def get_fields_by_area(
    area: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all fields in an area"""
    return await crud_field.get_fields_by_area(db=db, area=area)

@router.put("/{field_id}", response_model=Field)
async def update_field(
    field_id: str,
    field_in: FieldUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update field"""
    field = await crud_field.get(db=db, id=field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    return await crud_field.update(db=db, db_obj=field, obj_in=field_in)
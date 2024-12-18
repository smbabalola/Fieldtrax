# File: backend/app/api/v1/endpoints/tubular/tubular_type.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.jobsystem.tubular_type import crud_tubular_type
from app.schemas.jobsystem.tubular_type import (
    TubularTypeResponse as TubularType,
    TubularTypeCreate,
    TubularTypeUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=TubularType)
async def create_tubular_type(
    tubular_type_in: TubularTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new tubular type"""
    return await crud_tubular_type.create(db=db, obj_in=tubular_type_in)

@router.get("/", response_model=List[TubularType])
async def get_tubular_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all tubular types"""
    return await crud_tubular_type.get_multi(db=db, skip=skip, limit=limit)

@router.get("/type/{type_name}", response_model=TubularType)
async def get_tubular_type_by_name(
    type_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tubular type by name"""
    tubular_type = await crud_tubular_type.get_by_type(db=db, type_name=type_name)
    if not tubular_type:
        raise HTTPException(status_code=404, detail="Tubular type not found")
    return tubular_type

@router.get("/short/{short_name}", response_model=TubularType)
async def get_tubular_type_by_short_name(
    short_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tubular type by short name"""
    tubular_type = await crud_tubular_type.get_by_short_name(db=db, short_name=short_name)
    if not tubular_type:
        raise HTTPException(status_code=404, detail="Tubular type not found")
    return tubular_type

@router.put("/{type_id}", response_model=TubularType)
async def update_tubular_type(
    type_id: str,
    tubular_type_in: TubularTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update tubular type"""
    tubular_type = await crud_tubular_type.get(db=db, id=type_id)
    if not tubular_type:
        raise HTTPException(status_code=404, detail="Tubular type not found")
    return await crud_tubular_type.update(db=db, db_obj=tubular_type, obj_in=tubular_type_in)


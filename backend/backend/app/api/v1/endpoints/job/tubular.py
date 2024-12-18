# File: backend/app/api/v1/endpoints/tubular/tubular.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.tubular import crud_tubular
from app.schemas.jobsystem.tubular import (
    TubularResponse as Tubular,
    TubularCreate,
    TubularUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=Tubular)
async def create_tubular(
    tubular_in: TubularCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new tubular"""
    return await crud_tubular.create(db=db, obj_in=tubular_in)

@router.get("/type/{tubulartype_id}", response_model=List[Tubular])
async def get_tubulars_by_type(
    tubulartype_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tubulars by type"""
    return await crud_tubular.get_by_type(db=db, tubulartype_id=tubulartype_id)

@router.get("/thread/{thread}", response_model=List[Tubular])
async def get_tubulars_by_thread(
    thread: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tubulars by thread type"""
    return await crud_tubular.get_by_thread_type(db=db, thread=thread)

@router.get("/diameter-range", response_model=List[Tubular])
async def get_tubulars_by_diameter(
    min_od: float,
    max_od: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tubulars within outer diameter range"""
    return await crud_tubular.get_by_diameter_range(
        db=db,
        min_od=min_od,
        max_od=max_od
    )

@router.get("/depth-range", response_model=List[Tubular])
async def get_tubulars_by_depth(
    min_depth: float,
    max_depth: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tubulars within depth range"""
    return await crud_tubular.get_by_depth_range(
        db=db,
        min_depth=min_depth,
        max_depth=max_depth
    )

@router.put("/{tubular_id}", response_model=Tubular)
async def update_tubular(
    tubular_id: str,
    tubular_in: TubularUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update tubular"""
    tubular = await crud_tubular.get(db=db, id=tubular_id)
    if not tubular:
        raise HTTPException(status_code=404, detail="Tubular not found")
    return await crud_tubular.update(db=db, db_obj=tubular, obj_in=tubular_in)
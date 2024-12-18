# File: backend/app/api/v1/endpoints/wellbore/hanger_info.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.jobsystem.hanger_info import crud_hanger_info
from app.schemas.jobsystem.hanger_info import (
    HangerInfoResponse as HangerInfo,
    HangerInfoCreate,
    HangerInfoUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=HangerInfo)
async def create_hanger_info(
    hanger_in: HangerInfoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new hanger info"""
    try:
        return await crud_hanger_info.create(db=db, obj_in=hanger_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating hanger info: {str(e)}"
        )

@router.get("/", response_model=List[HangerInfo])
async def get_all_hangers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all hanger info with pagination"""
    return await crud_hanger_info.get_multi(db=db, skip=skip, limit=limit)

@router.get("/{hanger_id}", response_model=HangerInfo)
async def get_hanger_info(
    hanger_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get hanger info by ID"""
    hanger = await crud_hanger_info.get(db=db, id=hanger_id)
    if not hanger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hanger info not found"
        )
    return hanger

@router.get("/wellbore/{wellbore_id}", response_model=List[HangerInfo])
async def get_hangers_by_wellbore(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all hanger info for a wellbore"""
    return await crud_hanger_info.get_by_wellbore(db=db, wellbore_id=wellbore_id)

@router.get("/wellbore/{wellbore_id}/type/{hanger_type}", response_model=Optional[HangerInfo])
async def get_hanger_by_type(
    wellbore_id: str,
    hanger_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get hanger info by type for a wellbore"""
    hanger = await crud_hanger_info.get_by_type(
        db=db,
        wellbore_id=wellbore_id,
        hanger_type=hanger_type
    )
    if not hanger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hanger info found for type {hanger_type} in wellbore {wellbore_id}"
        )
    return hanger

@router.put("/{hanger_id}", response_model=HangerInfo)
async def update_hanger_info(
    hanger_id: str,
    hanger_in: HangerInfoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update hanger info"""
    hanger = await crud_hanger_info.get(db=db, id=hanger_id)
    if not hanger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hanger info not found"
        )
    try:
        return await crud_hanger_info.update(db=db, db_obj=hanger, obj_in=hanger_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating hanger info: {str(e)}"
        )

@router.delete("/{hanger_id}")
async def delete_hanger_info(
    hanger_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete hanger info"""
    hanger = await crud_hanger_info.get(db=db, id=hanger_id)
    if not hanger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hanger info not found"
        )
    try:
        await crud_hanger_info.remove(db=db, id=hanger_id)
        return {"message": "Hanger info deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting hanger info: {str(e)}"
        )

@router.get("/{hanger_id}/specifications")
async def get_hanger_specifications(
    hanger_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed specifications for a hanger"""
    hanger = await crud_hanger_info.get(db=db, id=hanger_id)
    if not hanger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hanger info not found"
        )
    
    return {
        "basic_info": {
            "type": hanger.type,
            "wellbore_id": hanger.wellbore_id
        },
        "ratings": {
            "burst_rating": hanger.burst_rating,
            "tensile_rating": hanger.tensile_rating,
            "hanging_capacity": hanger.hanging_capacity
        },
        "settings": {
            "hydraulic_setting_pressure": hanger.hydraulic_setting_pressure
        }
    }
# File: backend/app/api/v1/endpoints/logistics/backload.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.logisticsystem.backload import crud_backload
from app.schemas.logisticsystem.backload import (
    BackloadResponse,
    BackloadCreate,
    BackloadUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse

router = APIRouter()

@router.post("/", response_model=BackloadResponse)
async def create_backload(
    backload_in: BackloadCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Create new backload sheet"""
    return await crud_backload.create(db=db, obj_in=backload_in)

@router.get("/{backload_id}", response_model=BackloadResponse)
async def get_backload(
    backload_id: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get backload by ID"""
    backload = await crud_backload.get(db=db, id=backload_id)
    if not backload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backload not found"
        )
    return backload

@router.get("/wellbore/{wellbore_id}", response_model=List[BackloadResponse])
async def get_wellbore_backloads(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get all backloads for a wellbore"""
    return await crud_backload.get_by_wellbore(db=db, wellbore_id=wellbore_id)

@router.put("/{backload_id}", response_model=BackloadResponse)
async def update_backload(
    backload_id: str,
    backload_in: BackloadUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Update backload sheet"""
    backload = await crud_backload.get(db=db, id=backload_id)
    if not backload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backload not found"
        )
    return await crud_backload.update(db=db, db_obj=backload, obj_in=backload_in)

@router.post("/{backload_id}/approve")
async def approve_backload(
    backload_id: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Approve backload sheet"""
    backload = await crud_backload.approve_backload(
        db=db,
        backload_id=backload_id,
        approved_by=current_user.id
    )
    if not backload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backload not found"
        )
    return {"message": "Backload approved successfully"}

@router.get("/pending", response_model=List[BackloadResponse])
async def get_pending_backloads(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get all pending backloads"""
    return await crud_backload.get_pending_approvals(db=db)


# File: backend/app/api/v1/endpoints/wellbore/physical_barrier.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.physical_barrier import crud_physical_barrier
from app.schemas.jobsystem.physical_barrier import (
    PhysicalBarrierResponse as PhysicalBarrier,
    PhysicalBarrierCreate,
    PhysicalBarrierUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=PhysicalBarrier)
async def create_barrier(
    *,
    db: Session = Depends(get_db),
    barrier_in: PhysicalBarrierCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new physical barrier"""
    return await crud_physical_barrier.create(db=db, obj_in=barrier_in)

@router.get("/wellbore/{wellbore_id}", response_model=List[PhysicalBarrier])
async def get_barriers_by_wellbore(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all physical barriers for a wellbore"""
    return await crud_physical_barrier.get_by_wellbore(db=db, wellbore_id=wellbore_id)

@router.get("/wellbore/{wellbore_id}/verified", response_model=List[PhysicalBarrier])
async def get_verified_barriers(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get verified barriers for a wellbore"""
    return await crud_physical_barrier.get_verified_barriers(db=db, wellbore_id=wellbore_id)

@router.post("/{barrier_id}/verify")
async def verify_barrier(
    *,
    db: Session = Depends(get_db),
    barrier_id: str,
    current_user: User = Depends(get_current_user)
):
    """Mark a barrier as verified"""
    barrier = await crud_physical_barrier.mark_verified(
        db=db,
        barrier_id=barrier_id,
        verified_by=current_user.id
    )
    if not barrier:
        raise HTTPException(status_code=404, detail="Barrier not found")
    return {"message": "Barrier verified successfully"}

# File: backend/app/api/v1/endpoints/rig/rig_stability.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.rigsystem.rig_stability import crud_rig_stability
from app.schemas.rigsystem.rig_stability import (
    RigStability, RigStabilityCreate, RigStabilityUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import User

router = APIRouter()

@router.post("/", response_model=RigStability)
async def create_rig_stability(
    stability_in: RigStabilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new rig stability record"""
    return await crud_rig_stability.create(db=db, obj_in=stability_in)

@router.get("/rig/{rig_id}", response_model=RigStability)
async def get_stability_by_rig(
    rig_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get stability data for a rig"""
    stability = await crud_rig_stability.get_by_rig(db=db, rig_id=rig_id)
    if not stability:
        raise HTTPException(status_code=404, detail="Stability data not found")
    return stability

@router.get("/capacity/{min_deck_load}", response_model=List[RigStability])
async def get_rigs_by_capacity(
    min_deck_load: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get rigs by minimum deck load capacity"""
    return await crud_rig_stability.get_rigs_by_capacity(db=db, min_deck_load=min_deck_load)

@router.put("/{stability_id}", response_model=RigStability)
async def update_rig_stability(
    stability_id: str,
    stability_in: RigStabilityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update rig stability data"""
    stability = await crud_rig_stability.get(db=db, id=stability_id)
    if not stability:
        raise HTTPException(status_code=404, detail="Stability data not found")
    return await crud_rig_stability.update(db=db, db_obj=stability, obj_in=stability_in)
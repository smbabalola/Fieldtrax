# File: backend/app/api/v1/endpoints/installation/slot.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app.crud.jobsystem.slot import crud_slot
from app.schemas.jobsystem.slot import SlotResponse as Slot, SlotCreate, SlotUpdate
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=Slot)
async def create_slot(
    *,
    db: Session = Depends(get_db),
    slot_in: SlotCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new slot"""
    return await crud_slot.create(db=db, obj_in=slot_in)

@router.post("/batch", response_model=List[Slot])
async def batch_create_slots(
    *,
    db: Session = Depends(get_db),
    installation_id: str,
    slot_names: List[str],
    current_user: User = Depends(get_current_user)
):
    """Batch create multiple slots"""
    return await crud_slot.batch_create_slots(
        db=db,
        installation_id=installation_id,
        slot_names=slot_names
    )

@router.get("/installation/{installation_id}", response_model=List[Slot])
async def get_slots_by_installation(
    installation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all slots for an installation"""
    return await crud_slot.get_by_installation(db=db, installation_id=installation_id)

@router.get("/installation/{installation_id}/available", response_model=List[Slot])
async def get_available_slots(
    installation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get available slots for an installation"""
    return await crud_slot.get_available_slots(db=db, installation_id=installation_id)

@router.get("/installation/{installation_id}/with-wells", response_model=List[Slot])
async def get_slots_with_wells(
    installation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get slots that have wells"""
    return await crud_slot.get_slots_with_wells(db=db, installation_id=installation_id)

@router.get("/installation/{installation_id}/statistics", response_model=Dict)
async def get_slot_statistics(
    installation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get slot statistics for an installation"""
    return await crud_slot.get_slot_statistics(db=db, installation_id=installation_id)

@router.get("/coordinates", response_model=List[Slot])
async def get_slots_by_coordinates(
    min_eastings: float,
    max_eastings: float,
    min_northings: float,
    max_northings: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get slots within coordinate boundaries"""
    return await crud_slot.get_slots_by_coordinates(
        db=db,
        min_eastings=min_eastings,
        max_eastings=max_eastings,
        min_northings=min_northings,
        max_northings=max_northings
    )

@router.put("/{slot_id}/coordinates")
async def update_slot_coordinates(
    *,
    db: Session = Depends(get_db),
    slot_id: str,
    utm_eastings: float = None,
    utm_northings: float = None,
    latitude: str = None,
    longitude: str = None,
    current_user: User = Depends(get_current_user)
):
    """Update slot coordinates"""
    slot = await crud_slot.update_coordinates(
        db=db,
        slot_id=slot_id,
        utm_eastings=utm_eastings,
        utm_northings=utm_northings,
        latitude=latitude,
        longitude=longitude
    )
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    return slot
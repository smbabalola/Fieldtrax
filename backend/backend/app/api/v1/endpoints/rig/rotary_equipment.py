# File: backend/app/api/v1/endpoints/rig/rotary_equipment.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.rigsystem.rotary_equipment import crud_rotary_equipment
from app.schemas.rigsystem.rotary_equipment import (
    RotaryEquipmentResponse as RotaryEquipment, RotaryEquipmentCreate, RotaryEquipmentUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=RotaryEquipment)
async def create_rotary_equipment(
    equipment_in: RotaryEquipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new rotary equipment"""
    return await crud_rotary_equipment.create(db=db, obj_in=equipment_in)

@router.get("/rig/{rig_id}", response_model=RotaryEquipment)
async def get_equipment_by_rig(
    rig_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment for a rig"""
    equipment = await crud_rotary_equipment.get_by_rig(db=db, rig_id=rig_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.get("/manufacturer/{manufacturer}", response_model=List[RotaryEquipment])
async def get_equipment_by_manufacturer(
    manufacturer: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment by top drive manufacturer"""
    return await crud_rotary_equipment.get_by_manufacturer(db=db, manufacturer=manufacturer)

@router.get("/power/{min_power}", response_model=List[RotaryEquipment])
async def get_equipment_by_power(
    min_power: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment by minimum power rating"""
    return await crud_rotary_equipment.get_by_power_rating(db=db, min_power=min_power)

@router.put("/{equipment_id}", response_model=RotaryEquipment)
async def update_rotary_equipment(
    equipment_id: str,
    equipment_in: RotaryEquipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update rotary equipment"""
    equipment = await crud_rotary_equipment.get(db=db, id=equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return await crud_rotary_equipment.update(db=db, db_obj=equipment, obj_in=equipment_in)

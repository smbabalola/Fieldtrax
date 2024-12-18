# File: backend/app/api/v1/endpoints/rig/rig_equipment.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.rigsystem.rig_equipment import crud_rig_equipment
from app.schemas.rigsystem.rig_equipment import (
    RigEquipmentResponse as RigEquipment, RigEquipmentCreate, RigEquipmentUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=RigEquipment)
async def create_rig_equipment(
    equipment_in: RigEquipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new rig equipment"""
    return await crud_rig_equipment.create(db=db, obj_in=equipment_in)

@router.get("/rig/{rig_id}", response_model=RigEquipment)
async def get_equipment_by_rig(
    rig_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment for a rig"""
    equipment = await crud_rig_equipment.get_by_rig(db=db, rig_id=rig_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.get("/manufacturer/{manufacturer}", response_model=List[RigEquipment])
async def get_equipment_by_manufacturer(
    manufacturer: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment by manufacturer"""
    return await crud_rig_equipment.get_by_manufacturer(db=db, manufacturer=manufacturer)

@router.put("/{equipment_id}", response_model=RigEquipment)
async def update_rig_equipment(
    equipment_id: str,
    equipment_in: RigEquipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update rig equipment"""
    equipment = await crud_rig_equipment.get(db=db, id=equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return await crud_rig_equipment.update(db=db, db_obj=equipment, obj_in=equipment_in)
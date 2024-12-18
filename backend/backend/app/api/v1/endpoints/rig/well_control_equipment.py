# File: backend/app/api/v1/endpoints/rig/well_control_equipment.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.rigsystem.well_control_equipment import crud_well_control_equipment
from app.schemas.rigsystem.well_control_equipment import (
    WellControlEquipmentResponse as WellControlEquipment,
    WellControlEquipmentCreate,
    WellControlEquipmentUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=WellControlEquipment)
async def create_well_control_equipment(
    equipment_in: WellControlEquipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new well control equipment"""
    return await crud_well_control_equipment.create(db=db, obj_in=equipment_in)

@router.get("/rig/{rig_id}", response_model=WellControlEquipment)
async def get_equipment_by_rig(
    rig_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get well control equipment for a rig"""
    equipment = await crud_well_control_equipment.get_by_rig(db=db, rig_id=rig_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.get("/pressure/{min_pressure}", response_model=List[WellControlEquipment])
async def get_equipment_by_pressure(
    min_pressure: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment by minimum pressure rating"""
    return await crud_well_control_equipment.get_by_pressure_rating(db=db, min_pressure=min_pressure)

@router.get("/manufacturer/{manufacturer}", response_model=List[WellControlEquipment])
async def get_equipment_by_manufacturer(
    manufacturer: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment by diverter manufacturer"""
    return await crud_well_control_equipment.get_by_manufacturer(db=db, manufacturer=manufacturer)

@router.put("/{equipment_id}", response_model=WellControlEquipment)
async def update_well_control_equipment(
    equipment_id: str,
    equipment_in: WellControlEquipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update well control equipment"""
    equipment = await crud_well_control_equipment.get(db=db, id=equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return await crud_well_control_equipment.update(db=db, db_obj=equipment, obj_in=equipment_in)

@router.get("/{equipment_id}/specifications", response_model=dict)
async def get_equipment_specifications(
    equipment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed specifications for well control equipment"""
    equipment = await crud_well_control_equipment.get(db=db, id=equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    return {
        "bop_specifications": {
            "size": equipment.bop_size,
            "max_pressure": equipment.bop_max_pressure,
            "max_temperature": equipment.bop_max_temperature
        },
        "diverter_specifications": {
            "manufacturer": equipment.diverter_manufacturer,
            "model": equipment.diverter_model
        },
        "line_specifications": {
            "number": equipment.line_number,
            "internal_diameter": equipment.internal_diameter,
            "max_pressure": equipment.max_pressure,
            "length": equipment.line_length,
            "closing_time": equipment.closing_time
        },
        "choke_specifications": {
            "line_diameter": equipment.choke_line_diameter,
            "line_pressure": equipment.choke_line_pressure
        },
        "kill_specifications": {
            "line_diameter": equipment.kill_line_diameter
        }
    }
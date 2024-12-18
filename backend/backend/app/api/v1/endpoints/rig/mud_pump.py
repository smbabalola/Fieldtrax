# File: backend/app/api/v1/endpoints/rig/mud_pump.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.rigsystem.mud_pump import crud_mud_pump
from app.schemas.rigsystem.mud_pump import (
    MudPumpResponse as MudPump, MudPumpCreate, MudPumpUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=MudPump)
async def create_mud_pump(
    pump_in: MudPumpCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new mud pump"""
    return await crud_mud_pump.create(db=db, obj_in=pump_in)

@router.get("/rig/{rig_id}", response_model=List[MudPump])
async def get_pumps_by_rig(
    rig_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all mud pumps for a rig"""
    return await crud_mud_pump.get_by_rig(db=db, rig_id=rig_id)

@router.get("/serial/{serial_number}", response_model=MudPump)
async def get_pump_by_serial(
    serial_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get mud pump by serial number"""
    pump = await crud_mud_pump.get_by_serial_number(db=db, serial_number=serial_number)
    if not pump:
        raise HTTPException(status_code=404, detail="Mud pump not found")
    return pump

@router.get("/type/{pump_type}", response_model=List[MudPump])
async def get_pumps_by_type(
    pump_type: str,
    rig_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get mud pumps by type"""
    return await crud_mud_pump.get_by_type(
        db=db,
        pump_type=pump_type,
        rig_id=rig_id
    )

@router.put("/{pump_id}", response_model=MudPump)
async def update_mud_pump(
    pump_id: str,
    pump_in: MudPumpUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update mud pump"""
    pump = await crud_mud_pump.get(db=db, id=pump_id)
    if not pump:
        raise HTTPException(status_code=404, detail="Mud pump not found")
    return await crud_mud_pump.update(db=db, db_obj=pump, obj_in=pump_in)
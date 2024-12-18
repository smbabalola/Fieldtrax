# File: backend/app/api/v1/endpoints/job/mud_pump_detail.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.mud_pump_detail import crud_mud_pump_detail
from app.schemas.jobsystem.mud_pump_detail import (
    MudPumpDetailResponse, MudPumpDetailCreate, MudPumpDetailUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=MudPumpDetailResponse)
async def create_mud_pump(
    *,
    db: Session = Depends(get_db),
    pump_in: MudPumpDetailCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new mud pump detail"""
    return await crud_mud_pump_detail.create(db=db, obj_in=pump_in)

@router.get("/report/{report_id}", response_model=List[MudPumpDetailResponse])
async def get_pumps_by_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all mud pump details for a report"""
    return await crud_mud_pump_detail.get_by_report(db=db, report_id=report_id)

@router.get("/report/{report_id}/active", response_model=List[MudPumpDetailResponse])
async def get_active_pumps(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get active mud pumps for a report"""
    return await crud_mud_pump_detail.get_active_pumps(db=db, report_id=report_id)

@router.put("/{pump_id}", response_model=MudPumpDetailResponse)
async def update_mud_pump(
    *,
    db: Session = Depends(get_db),
    pump_id: str,
    pump_in: MudPumpDetailUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update mud pump detail"""
    pump = await crud_mud_pump_detail.get(db=db, id=pump_id)
    if not pump:
        raise HTTPException(status_code=404, detail="Mud pump not found")
    return await crud_mud_pump_detail.update(db=db, db_obj=pump, obj_in=pump_in)
# File: backend/app/api/v1/endpoints/job/mud_equipment_detail.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.mud_equipment_detail import crud_mud_equipment_detail
from app.models.authsystem.user import User
from app.schemas.jobsystem.mud_equipment_detail import (
    MudEquipmentDetailResponse, MudEquipmentDetailCreate, MudEquipmentDetailUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse

router = APIRouter()

@router.post("/", response_model=MudEquipmentDetailResponse)
async def create_mud_equipment(
    *,
    db: Session = Depends(get_db),
    equipment_in: MudEquipmentDetailCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new mud equipment detail"""
    return await crud_mud_equipment_detail.create(db=db, obj_in=equipment_in)

@router.get("/report/{report_id}", response_model=List[MudEquipmentDetailResponse])
async def get_equipment_by_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all mud equipment details for a report"""
    return await crud_mud_equipment_detail.get_by_report(db=db, report_id=report_id)

@router.put("/{equipment_id}", response_model=MudEquipmentDetailResponse)
async def update_mud_equipment(
    *,
    db: Session = Depends(get_db),
    equipment_id: str,
    equipment_in: MudEquipmentDetailUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update mud equipment detail"""
    equipment = await crud_mud_equipment_detail.get(db=db, id=equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Mud equipment not found")
    return await crud_mud_equipment_detail.update(db=db, db_obj=equipment, obj_in=equipment_in)

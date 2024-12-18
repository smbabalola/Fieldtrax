# File: backend/app/api/v1/endpoints/operations/operational_parameter.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.operational_parameter import crud_operational_parameter
from app.schemas.jobsystem.operational_parameter import (
    OperationalParameterResponse as OperationalParameter,
    OperationalParameterCreate,
    OperationalParameterUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=OperationalParameter)
async def create_operational_parameter(
    *,
    db: Session = Depends(get_db),
    param_in: OperationalParameterCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new operational parameter"""
    return await crud_operational_parameter.create(db=db, obj_in=param_in)

@router.get("/wellbore/{wellbore_id}", response_model=List[OperationalParameter])
async def get_parameters_by_wellbore(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all operational parameters for a wellbore"""
    return await crud_operational_parameter.get_by_wellbore(db=db, wellbore_id=wellbore_id)

@router.get("/wellbore/{wellbore_id}/zone/{zone}", response_model=OperationalParameter)
async def get_parameters_by_zone(
    wellbore_id: str,
    zone: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get operational parameters for a specific zone"""
    param = await crud_operational_parameter.get_by_zone(db=db, wellbore_id=wellbore_id, zone=zone)
    if not param:
        raise HTTPException(status_code=404, detail="Parameters not found")
    return param
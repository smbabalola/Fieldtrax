# File: backend/app/api/v1/endpoints/wellbore/job_parameter.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.job_parameter import crud_job_parameter
from app.schemas.jobsystem.job_parameter import (
    JobParameterResponse as JobParameter, JobParameterCreate, JobParameterUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=JobParameter)
async def create_job_parameter(
    *,
    db: Session = Depends(get_db),
    param_in: JobParameterCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new run parameter"""
    return await crud_job_parameter.create(db=db, obj_in=param_in)

@router.get("/wellbore/{wellbore_id}", response_model=List[JobParameter])
async def get_parameters_by_wellbore(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all run parameters for a wellbore"""
    return await crud_job_parameter.get_by_wellbore(db=db, wellbore_id=wellbore_id)

@router.put("/{param_id}", response_model=JobParameter)
async def update_job_parameter(
    *,
    db: Session = Depends(get_db),
    param_id: str,
    param_in: JobParameterUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update run parameter"""
    param = await crud_job_parameter.get(db=db, id=param_id)
    if not param:
        raise HTTPException(status_code=404, detail="Run parameter not found")
    return await crud_job_parameter.update(db=db, db_obj=param, obj_in=param_in)


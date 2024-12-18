# File: backend/app/api/v1/endpoints/job/job_center.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.jobsystem.job_center import crud_job_center
from app.schemas.jobsystem.job_center import JobCenterResponse as JobCenter, JobCenterCreate, JobCenterUpdate
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=JobCenter)
async def create_job_center(
    center_in: JobCenterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new job center"""
    return await crud_job_center.create(db=db, obj_in=center_in)

@router.get("/well/{well_name}", response_model=JobCenter)
async def get_job_center_by_well(
    well_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get job center by well name"""
    center = await crud_job_center.get_by_well_name(db=db, well_name=well_name)
    if not center:
        raise HTTPException(status_code=404, detail="Job center not found")
    return center

@router.get("/short/{short_name}", response_model=JobCenter)
async def get_job_center_by_short_name(
    short_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get job center by short name"""
    center = await crud_job_center.get_by_short_name(db=db, short_name=short_name)
    if not center:
        raise HTTPException(status_code=404, detail="Job center not found")
    return center

@router.get("/active", response_model=List[JobCenter])
async def get_active_job_centers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all active job centers"""
    return await crud_job_center.get_active_job_centers(db=db)

@router.put("/{center_id}", response_model=JobCenter)
async def update_job_center(
    center_id: str,
    center_in: JobCenterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update job center"""
    center = await crud_job_center.get(db=db, id=center_id)
    if not center:
        raise HTTPException(status_code=404, detail="Job center not found")
    return await crud_job_center.update(db=db, db_obj=center, obj_in=center_in)


# In job_center.py
@router.get("/", response_model=List[JobCenter])
async def get_job_centers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get all job centers"""
    return await crud_job_center.get_multi(db=db, skip=skip, limit=limit)


# Add exports
__all__ = ['router']
# File: backend/app/api/v1/endpoints/job/activity.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.crud.jobsystem.activity import crud_activity
from app.schemas.jobsystem.activity import (
    ActivityResponse as Activity, ActivityCreate, ActivityUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=Activity)
async def create_activity(
    report_in: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new daily report"""
    return await crud_activity.create(db=db, obj_in=report_in)

@router.get("/wellbore/{job_id}", response_model=List[Activity])
async def get_wellbore_reports(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all daily reports for a wellbore"""
    return await crud_activity.get_by_wellbore(db=db, job_id=job_id)

@router.get("/wellbore/{wellbore_id}/date-range", response_model=List[Activity])
async def get_reports_by_date(
    job_id: str,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get daily reports within date range"""
    return await crud_activity.get_by_date_range(
        db=db,
        wellbore_id=job_id,
        start_date=start_date,
        end_date=end_date
    )

@router.put("/{activity_id}", response_model=Activity)
async def update_activity(
    activity_id: str,
    activity_in: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update daily report"""
    activity = await crud_activity.get(db=db, id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Daily report not found")
    return await crud_activity.update(db=db, db_obj=activity, obj_in=activity_in)
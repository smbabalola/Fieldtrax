# File: backend/app/api/v1/endpoints/job/daily_report.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.crud.jobsystem.daily_report import crud_daily_report
from app.schemas.jobsystem.daily_report import (
    DailyReportResponse as DailyReport, DailyReportCreate, DailyReportUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=DailyReport)
async def create_daily_report(
    report_in: DailyReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new daily report"""
    return await crud_daily_report.create(db=db, obj_in=report_in)

@router.get("/wellbore/{wellbore_id}", response_model=List[DailyReport])
async def get_wellbore_reports(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all daily reports for a wellbore"""
    return await crud_daily_report.get_by_wellbore(db=db, wellbore_id=wellbore_id)

@router.get("/wellbore/{wellbore_id}/date-range", response_model=List[DailyReport])
async def get_reports_by_date(
    wellbore_id: str,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get daily reports within date range"""
    return await crud_daily_report.get_by_date_range(
        db=db,
        wellbore_id=wellbore_id,
        start_date=start_date,
        end_date=end_date
    )

@router.put("/{report_id}", response_model=DailyReport)
async def update_daily_report(
    report_id: str,
    report_in: DailyReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update daily report"""
    report = await crud_daily_report.get(db=db, id=report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Daily report not found")
    return await crud_daily_report.update(db=db, db_obj=report, obj_in=report_in)
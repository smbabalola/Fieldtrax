# File: backend/app/api/v1/endpoints/timesheet/time_sheet.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.crud.jobsystem.time_sheet import crud_time_sheet
from app.schemas.jobsystem.time_sheet import TimeSheetResponse as TimeSheet, TimeSheetCreate, TimeSheetUpdate
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=TimeSheet)
async def create_time_sheet(
    *,
    db: Session = Depends(get_db),
    timesheet_in: TimeSheetCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new time sheet"""
    return await crud_time_sheet.create(db=db, obj_in=timesheet_in)

@router.get("/job/{job_id}", response_model=List[TimeSheet])
async def get_time_sheets_by_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all time sheets for a job"""
    return await crud_time_sheet.get_by_job(db=db, job_id=job_id)

@router.get("/employee/{employee_id}", response_model=List[TimeSheet])
async def get_time_sheets_by_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all time sheets for an employee"""
    return await crud_time_sheet.get_by_employee(db=db, employee_id=employee_id)

@router.get("/pending", response_model=List[TimeSheet])
async def get_pending_time_sheets(
    job_id: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get time sheets pending approval"""
    return await crud_time_sheet.get_pending_approval(db=db, job_id=job_id)

@router.post("/{timesheet_id}/approve", response_model=TimeSheet)
async def approve_time_sheet(
    timesheet_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Approve a time sheet"""
    timesheet = await crud_time_sheet.approve_timesheet(
        db=db,
        timesheet_id=timesheet_id,
        approved_by=current_user.id
    )
    if not timesheet:
        raise HTTPException(status_code=404, detail="Time sheet not found")
    return timesheet

@router.get("/date-range", response_model=List[TimeSheet])
async def get_time_sheets_by_date(
    start_date: datetime,
    end_date: datetime,
    employee_id: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get time sheets within date range"""
    return await crud_time_sheet.get_by_date_range(
        db=db,
        start_date=start_date,
        end_date=end_date,
        employee_id=employee_id
    )

@router.get("/hours/total")
async def calculate_total_hours(
    employee_id: str,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate total hours worked in date range"""
    total_hours = await crud_time_sheet.calculate_total_hours(
        db=db,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date
    )
    return {"total_hours": total_hours}

@router.put("/{timesheet_id}", response_model=TimeSheet)
async def update_time_sheet(
    *,
    db: Session = Depends(get_db),
    timesheet_id: str,
    timesheet_in: TimeSheetUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update time sheet"""
    timesheet = await crud_time_sheet.get(db=db, id=timesheet_id)
    if not timesheet:
        raise HTTPException(status_code=404, detail="Time sheet not found")
    return await crud_time_sheet.update(db=db, db_obj=timesheet, obj_in=timesheet_in)
# File: backend/app/crud/jobsystem/crud_time_sheet.py
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.time_sheet import TimeSheet
from app.schemas.jobsystem.time_sheet import TimeSheetCreate, TimeSheetUpdate

class CRUDTimeSheet(CRUDBase[TimeSheet, TimeSheetCreate, TimeSheetUpdate]):
    async def get_by_job(
        self,
        db: Session,
        *,
        job_id: str
    ) -> List[TimeSheet]:
        """Get all time sheets for a job"""
        return db.query(TimeSheet).filter(
            TimeSheet.job_id == job_id
        ).order_by(TimeSheet.date.desc()).all()

    async def get_by_employee(
        self,
        db: Session,
        *,
        employee_id: str
    ) -> List[TimeSheet]:
        """Get all time sheets for an employee"""
        return db.query(TimeSheet).filter(
            TimeSheet.employee_id == employee_id
        ).order_by(TimeSheet.date.desc()).all()

    async def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
        employee_id: Optional[str] = None
    ) -> List[TimeSheet]:
        """Get time sheets within date range"""
        query = db.query(TimeSheet).filter(
            TimeSheet.date >= start_date,
            TimeSheet.date <= end_date
        )
        if employee_id:
            query = query.filter(TimeSheet.employee_id == employee_id)
        return query.order_by(TimeSheet.date.desc()).all()

    async def get_pending_approval(
        self,
        db: Session,
        *,
        job_id: Optional[str] = None
    ) -> List[TimeSheet]:
        """Get time sheets pending approval"""
        query = db.query(TimeSheet).filter(
            TimeSheet.approved.is_(False)
        )
        if job_id:
            query = query.filter(TimeSheet.job_id == job_id)
        return query.order_by(TimeSheet.date.desc()).all()

    async def approve_timesheet(
        self,
        db: Session,
        *,
        timesheet_id: str,
        approved_by: str
    ) -> Optional[TimeSheet]:
        """Approve a timesheet"""
        timesheet = await self.get(db=db, id=timesheet_id)
        if timesheet:
            timesheet.approved = True
            timesheet.approved_by = approved_by
            timesheet.approval_date = datetime.utcnow()
            db.add(timesheet)
            db.commit()
            db.refresh(timesheet)
        return timesheet

    async def calculate_total_hours(
        self,
        db: Session,
        *,
        employee_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> float:
        """Calculate total hours worked in date range"""
        timesheets = await self.get_by_date_range(
            db=db,
            start_date=start_date,
            end_date=end_date,
            employee_id=employee_id
        )
        return sum(ts.hours_worked for ts in timesheets)


crud_time_sheet = CRUDTimeSheet(TimeSheet)

# from app.models.jobsystem.time_sheet import TimeSheet
# from app.crud.base import CRUDBase

# crud_time_sheet = CRUDBase(TimeSheet)
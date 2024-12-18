# File: backend/app/crud/jobsystem/crud_daily_report.py
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_, func
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.base import CRUDBase
from app.models.jobsystem.daily_report import DailyReport
from app.schemas.jobsystem.daily_report import DailyReportCreate, DailyReportUpdate

class CRUDDailyReport(CRUDBase[DailyReport, DailyReportCreate, DailyReportUpdate]):
    async def get_by_wellbore(
        self, 
        db: Session, 
        *, 
        wellbore_id: str,
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False
    ) -> List[DailyReport]:
        """Get all daily reports for a wellbore with pagination"""
        try:
            query = db.query(DailyReport).filter(
                DailyReport.wellbore_id == wellbore_id
            )
            
            if not include_inactive and hasattr(DailyReport, 'is_active'):
                query = query.filter(DailyReport.is_active == True)
                
            return query.order_by(desc(DailyReport.report_date))\
                       .offset(skip)\
                       .limit(limit)\
                       .all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_by_date_range(
        self, 
        db: Session, 
        *, 
        wellbore_id: str,
        start_date: datetime,
        end_date: datetime,
        status: Optional[str] = None
    ) -> List[DailyReport]:
        """Get daily reports within a date range with optional status filter"""
        try:
            query = db.query(DailyReport).filter(
                and_(
                    DailyReport.wellbore_id == wellbore_id,
                    DailyReport.report_date >= start_date,
                    DailyReport.report_date <= end_date
                )
            )
            
            if status:
                query = query.filter(DailyReport.status == status)
                
            return query.order_by(desc(DailyReport.report_date)).all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_latest_report(
        self, 
        db: Session, 
        *, 
        wellbore_id: str
    ) -> Optional[DailyReport]:
        """Get the latest daily report for a wellbore"""
        try:
            return db.query(DailyReport)\
                    .filter(DailyReport.wellbore_id == wellbore_id)\
                    .order_by(desc(DailyReport.report_date))\
                    .first()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_reports_summary(
        self,
        db: Session,
        *,
        wellbore_id: str,
        last_n_days: int = 30
    ) -> Dict[str, Any]:
        """Get summary statistics for daily reports"""
        try:
            start_date = datetime.utcnow() - timedelta(days=last_n_days)
            
            reports = db.query(DailyReport)\
                       .filter(
                           and_(
                               DailyReport.wellbore_id == wellbore_id,
                               DailyReport.report_date >= start_date
                           )
                       ).all()
            
            return {
                "total_reports": len(reports),
                "report_dates": [r.report_date for r in reports],
                "status_counts": self._count_status(reports),
                "latest_report": reports[0] if reports else None
            }
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def search_reports(
        self,
        db: Session,
        *,
        wellbore_id: str,
        search_term: str,
        fields: List[str] = ['comments', 'operations', 'status']
    ) -> List[DailyReport]:
        """Search daily reports by multiple fields"""
        try:
            filters = []
            for field in fields:
                if hasattr(DailyReport, field):
                    filters.append(
                        getattr(DailyReport, field).ilike(f"%{search_term}%")
                    )
            
            return db.query(DailyReport)\
                    .filter(
                        and_(
                            DailyReport.wellbore_id == wellbore_id,
                            or_(*filters)
                        )
                    )\
                    .order_by(desc(DailyReport.report_date))\
                    .all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_reports_by_status(
        self,
        db: Session,
        *,
        wellbore_id: str,
        status: str
    ) -> List[DailyReport]:
        """Get all reports with a specific status"""
        try:
            return db.query(DailyReport)\
                    .filter(
                        and_(
                            DailyReport.wellbore_id == wellbore_id,
                            DailyReport.status == status
                        )
                    )\
                    .order_by(desc(DailyReport.report_date))\
                    .all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def _count_status(self, reports: List[DailyReport]) -> Dict[str, int]:
        """Helper method to count reports by status"""
        status_counts = {}
        for report in reports:
            status_counts[report.status] = status_counts.get(report.status, 0) + 1
        return status_counts

crud_daily_report = CRUDDailyReport(DailyReport)

# from app.models.jobsystem.daily_report import DailyReport
# from app.crud.base import CRUDBase

# crud_daily_report = CRUDBase(DailyReport)
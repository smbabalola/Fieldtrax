# File: backend/app/crud/jobsystem/crud_activity.py
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_, func
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.base import CRUDBase
from app.models.jobsystem.activity import Activity
from app.schemas.jobsystem.activity import ActivityCreate, ActivityUpdate

class CRUDActivity(CRUDBase[Activity, ActivityCreate, ActivityUpdate]):
    async def get_by_job(
        self, 
        db: Session, 
        *, 
        job_id: str,
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False
    ) -> List[Activity]:
        """Get all activities for an activity with pagination"""
        try:
            query = db.query(Activity).filter(
                Activity.job_id == job_id
            )
            
            if not include_inactive and hasattr(Activity, 'is_active'):
                query = query.filter(Activity.is_active == True)
                
            return query.order_by(desc(Activity.timestamp))\
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
        job_id: str,
        start_date: datetime,
        end_date: datetime,
        status: Optional[str] = None
    ) -> List[Activity]:
        """Get Activity reports within a date range with optional status filter"""
        try:
            query = db.query(Activity).filter(
                and_(
                    Activity.job_id == job_id,
                    Activity.timestamp >= start_date,
                    Activity.timestamp <= end_date
                )
            )
            
            if status:
                query = query.filter(Activity.status == status)
                
            return query.order_by(desc(Activity.timestamp)).all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_latest_activity(
        self, 
        db: Session, 
        *, 
        job_id: str
    ) -> Optional[Activity]:
        """Get the latest activity for a job"""
        try:
            return db.query(Activity)\
                    .filter(Activity.job_id == job_id)\
                    .order_by(desc(Activity.timestamp))\
                    .first()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_activities_summary(
        self,
        db: Session,
        *,
        job_id: str,
        last_n_days: int = 30
    ) -> Dict[str, Any]:
        """Get summary statistics for activities"""
        try:
            start_date = datetime.utcnow() - timedelta(days=last_n_days)
            
            reports = db.query(Activity)\
                       .filter(
                           and_(
                               Activity.job_id == job_id,
                               Activity.timestamp >= start_date
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

    async def search_activities(
        self,
        db: Session,
        *,
        job_id: str,
        search_term: str,
        fields: List[str] = ["mobilization", "demobilization", "equipment_delivery", "start_job", "end_job", "incident","NPT"]
    ) -> List[Activity]:
        """Search daily reports by multiple fields"""
        try:
            filters = []
            for field in fields:
                if hasattr(Activity, field):
                    filters.append(
                        getattr(Activity, field).ilike(f"%{search_term}%")
                    )
            
            return db.query(Activity)\
                    .filter(
                        and_(
                            Activity.job_id == job_id,
                            or_(*filters)
                        )
                    )\
                    .order_by(desc(Activity.timestamp))\
                    .all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_reports_by_types(
        self,
        db: Session,
        *,
        job_id: str,
        status: str
    ) -> List[Activity]:
        """Get all reports with a specific status"""
        try:
            return db.query(Activity)\
                    .filter(
                        and_(
                            Activity.job_id == job_id,
                            Activity.type == status
                        )
                    )\
                    .order_by(desc(Activity.timestamp))\
                    .all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def _count_status(self, reports: List[Activity]) -> Dict[str, int]:
        """Helper method to count reports by status"""
        status_counts = {}
        for report in reports:
            status_counts[report.status] = status_counts.get(report.status, 0) + 1
        return status_counts

crud_activity = CRUDActivity(Activity)
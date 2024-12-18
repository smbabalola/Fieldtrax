# File: backend/app/crud/jobsystem/crud_job_center.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.job_center import JobCenter
from app.schemas.jobsystem.job_center import JobCenterCreate, JobCenterUpdate

class CRUDJobCenter(CRUDBase[JobCenter, JobCenterCreate, JobCenterUpdate]):
    async def get_by_well_name(
        self, 
        db: Session, 
        *, 
        well_name: str
    ) -> Optional[JobCenter]:
        """Get job center by well name"""
        return db.query(JobCenter).filter(
            JobCenter.well_name == well_name
        ).first()

    async def get_by_short_name(
        self, 
        db: Session, 
        *, 
        short_name: str
    ) -> Optional[JobCenter]:
        """Get job center by short name"""
        return db.query(JobCenter).filter(
            JobCenter.short_name == short_name
        ).first()

    async def get_active_job_centers(
        self, 
        db: Session
    ) -> List[JobCenter]:
        """Get all active job centers"""
        return db.query(JobCenter).filter(
            db.exists().where(
                JobCenter.jobs.any(job_closed=False)
            )
        ).all()

crud_job_center = CRUDJobCenter(JobCenter)

# from app.models.jobsystem.job_center import JobCenter
# from app.crud.base import CRUDBase

# crud_job_center = CRUDBase(JobCenter)
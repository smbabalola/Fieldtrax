from typing import List, Optional, Union, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.job import Job
from app.schemas.jobsystem.job import JobCreate, JobUpdate

class CRUDJob(CRUDBase[Job, JobCreate, JobUpdate]):
    async def get_by_well(self, db: Session, *, well_id: str) -> List[Job]:
        """Get all jobs for a specific well"""
        return db.query(Job).filter(Job.well_id == well_id).all()
    
    async def get_active_jobs(self, db: Session) -> List[Job]:
        """Get all active jobs"""
        return db.query(Job).filter(Job.job_closed == False).all()
    
    async def get_jobs_by_operator(self, db: Session, *, operator_id: str) -> List[Job]:
        """Get all jobs for a specific operator"""
        return db.query(Job).filter(Job.operator_id == operator_id).all()

    async def close_job(self, db: Session, *, job_id: str) -> Optional[Job]:
        """Close a job"""
        job = await self.get(db=db, id=job_id)
        if job:
            job.job_closed = True
            job.updated_at = datetime.utcnow()
            db.add(job)
            db.commit()
            db.refresh(job)
        return job

    async def get_multi(self, db: Session, skip: int = 0, limit: int = 100, filters: Dict[str, Any] = None) -> List[Job]:
        query = db.query(Job)
        
        if filters:
            if filters.get("status") and filters["status"] != "ALL":
                query = query.filter(Job.status == filters["status"])
            if filters.get("search_term"):
                search_term = f"%{filters['search_term']}%"
                query = query.filter(Job.description.ilike(search_term) | Job.job_number.ilike(search_term) | Job.notes.ilike(search_term))
            if filters.get("sort_field") and filters.get("sort_order"):
                sort_field = getattr(Job, filters["sort_field"])
                if filters["sort_order"] == "desc":
                    sort_field = sort_field.desc()
                query = query.order_by(sort_field)
        
        return query.offset(skip).limit(limit).all()

crud_job = CRUDJob(Job)
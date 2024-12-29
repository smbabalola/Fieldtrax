# File: backend/app/crud/jobsystem/crud_cmt_job.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.cmt_job import Cmt_job
from app.schemas.jobsystem.cmt_job import Cmt_jobCreate, Cmt_jobUpdate

class CRUDCmt_job(CRUDBase[Cmt_job, Cmt_jobCreate, Cmt_jobUpdate]):
    async def get_by_field(
        self, 
        db: Session, 
        *, 
        field_id: str
    ) -> List[Cmt_job]:
        """Get all cmt_jobs in a field"""
        return db.query(Cmt_job).filter(
            Cmt_job.field_id == field_id
        ).all()

    async def get_by_name(
        self, 
        db: Session, 
        *, 
        cmt_job_name: str
    ) -> Optional[Cmt_job]:
        """Get cmt_job by name"""
        return db.query(Cmt_job).filter(
            Cmt_job.cmt_job_name == cmt_job_name
        ).first()

    async def get_by_type(
        self, 
        db: Session, 
        *, 
        cmt_job_type_id: str
    ) -> List[Cmt_job]:
        """Get cmt_jobs by type"""
        return db.query(Cmt_job).filter(
            Cmt_job.cmt_job_type_id == cmt_job_type_id
        ).all()

crud_cmt_job = CRUDCmt_job(Cmt_job)
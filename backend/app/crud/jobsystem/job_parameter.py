# File: backend/app//jobsystem/_job_parameter.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.job_parameter import JobParameter
from app.schemas.jobsystem.job_parameter import (
    JobParameterCreate, 
    JobParameterUpdate
)

class CRUDJobParameter(CRUDBase[JobParameter, JobParameterCreate, JobParameterUpdate]):
    async def get_by_wellbore(
        self, 
        db: Session, 
        *, 
        wellbore_id: str
    ) -> List[JobParameter]:
        """Get all run parameters for a wellbore"""
        return db.query(JobParameter).filter(
            JobParameter.wellbore_id == wellbore_id
        ).all()

crud_job_parameter = CRUDJobParameter(JobParameter)

# from app.models.jobsystem.job_parameter import JobParameter
# from app.crud.base import CRUDBase

# crud_job_parameter = CRUDBase(JobParameter)
# File: backend/app/crud/jobsystem/crud_operational_parameter.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.operational_parameter import OperationalParameter
from app.schemas.jobsystem.operational_parameter import (
    OperationalParameterCreate, 
    OperationalParameterUpdate
)

class CRUDOperationalParameter(CRUDBase[OperationalParameter, OperationalParameterCreate, OperationalParameterUpdate]):
    async def get_by_wellbore(
        self, 
        db: Session, 
        *, 
        wellbore_id: str
    ) -> List[OperationalParameter]:
        """Get all operational parameters for a wellbore"""
        return db.query(OperationalParameter).filter(
            OperationalParameter.wellbore_id == wellbore_id
        ).all()

    async def get_by_zone(
        self, 
        db: Session, 
        *, 
        wellbore_id: str,
        zone: str
    ) -> Optional[OperationalParameter]:
        """Get operational parameters for a specific zone"""
        return db.query(OperationalParameter).filter(
            OperationalParameter.wellbore_id == wellbore_id,
            OperationalParameter.zone == zone
        ).first()

crud_operational_parameter = CRUDOperationalParameter(OperationalParameter)

# from app.models.jobsystem.operational_parameter import OperationalParameter
# from app.crud.base import CRUDBase

# crud_operational_paremeter = CRUDBase(OperationalParameter)

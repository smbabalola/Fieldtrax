# File: backend/app/crud/rigsystem/crud_rig.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.rigsystem.rig import Rig
from app.schemas.rigsystem.rig import RigCreate, RigUpdate

class CRUDRig(CRUDBase[Rig, RigCreate, RigUpdate]):
    async def get_by_name(
        self,
        db: Session,
        *,
        rig_name: str
    ) -> Optional[Rig]:
        """Get rig by name"""
        return db.query(Rig).filter(
            Rig.rig_name == rig_name
        ).first()

    async def get_by_contractor(
        self,
        db: Session,
        *,
        contractor_id: int
    ) -> List[Rig]:
        """Get all rigs for a contractor"""
        return db.query(Rig).filter(
            Rig.contractor_id == contractor_id
        ).all()

    async def get_by_type(
        self,
        db: Session,
        *,
        rig_type_id: int
    ) -> List[Rig]:
        """Get rigs by type"""
        return db.query(Rig).filter(
            Rig.rig_type_id == rig_type_id
        ).all()

    async def get_active_rigs(
        self,
        db: Session
    ) -> List[Rig]:
        """Get all rigs with active jobs"""
        return db.query(Rig).filter(
            Rig.jobs.any(job_closed=False)
        ).all()
        
crud_rig = CRUDRig(Rig)

# from app.models.rigsystem.rig import Rig
# from app.crud.base import CRUDBase

# crud_rig = CRUDBase(Rig)
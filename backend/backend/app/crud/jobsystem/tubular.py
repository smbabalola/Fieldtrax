# File: backend/app/crud/jobsystem/crud_tubular.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.tubular import Tubular
from app.schemas.jobsystem.tubular import TubularCreate, TubularUpdate

class CRUDTubular(CRUDBase[Tubular, TubularCreate, TubularUpdate]):
    async def get_by_type(
        self,
        db: Session,
        *,
        tubulartype_id: str
    ) -> List[Tubular]:
        """Get tubulars by type"""
        return db.query(Tubular).filter(
            Tubular.tubulartype_id == tubulartype_id
        ).all()

    async def get_by_thread_type(
        self,
        db: Session,
        *,
        thread: str
    ) -> List[Tubular]:
        """Get tubulars by thread type"""
        return db.query(Tubular).filter(
            Tubular.thread == thread
        ).all()

    async def get_by_diameter_range(
        self,
        db: Session,
        *,
        min_od: float,
        max_od: float
    ) -> List[Tubular]:
        """Get tubulars within outer diameter range"""
        return db.query(Tubular).filter(
            Tubular.outer_diameter >= min_od,
            Tubular.outer_diameter <= max_od
        ).all()

    async def get_by_depth_range(
        self,
        db: Session,
        *,
        min_depth: float,
        max_depth: float
    ) -> List[Tubular]:
        """Get tubulars within depth range"""
        return db.query(Tubular).filter(
            Tubular.start_depth >= min_depth,
            Tubular.end_depth <= max_depth
        ).all()

crud_tubular = CRUDTubular(Tubular)

# from app.models.jobsystem.tubular import Tubular
# from app.crud.base import CRUDBase

# crud_tubular = CRUDBase(Tubular)
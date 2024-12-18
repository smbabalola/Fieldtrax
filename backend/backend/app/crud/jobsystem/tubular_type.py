# File: backend/app/crud/jobsystem/crud_tubular_type.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.tubular_type import TubularType
from app.schemas.jobsystem.tubular_type import TubularTypeCreate, TubularTypeUpdate

class CRUDTubularType(CRUDBase[TubularType, TubularTypeCreate, TubularTypeUpdate]):
    async def get_by_type(
        self,
        db: Session,
        *,
        type_name: str
    ) -> Optional[TubularType]:
        """Get tubular type by name"""
        return db.query(TubularType).filter(
            TubularType.type == type_name
        ).first()

    async def get_by_short_name(
        self,
        db: Session,
        *,
        short_name: str
    ) -> Optional[TubularType]:
        """Get tubular type by short name"""
        return db.query(TubularType).filter(
            TubularType.type_short == short_name
        ).first()

crud_tubular_type = CRUDTubularType(TubularType)

# from app.models.jobsystem.tubular_type import TubularType
# from app.crud.base import CRUDBase

# crud_tubular_type = CRUDBase(TubularType)
# File: backend/app/crud/jobsystem/crud_hanger_info.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.hanger_info import HangerInfo
from app.schemas.jobsystem.hanger_info import HangerInfoCreate, HangerInfoUpdate

class CRUDHangerInfo(CRUDBase[HangerInfo, HangerInfoCreate, HangerInfoUpdate]):
    async def get_by_wellbore(self, db: Session, *, wellbore_id: str) -> List[HangerInfo]:
        """Get all hanger info for a wellbore"""
        return db.query(HangerInfo).filter(HangerInfo.wellbore_id == wellbore_id).all()

    async def get_by_type(
        self, 
        db: Session, 
        *, 
        wellbore_id: str,
        hanger_type: str
    ) -> Optional[HangerInfo]:
        """Get hanger info by type"""
        return db.query(HangerInfo).filter(
            HangerInfo.wellbore_id == wellbore_id,
            HangerInfo.type == hanger_type
        ).first()
        
crud_hanger_info = CRUDHangerInfo(HangerInfo)

# from app.models.jobsystem.hanger_info import HangerInfo
# from app.crud.base import CRUDBase

# crud_hanger_info = CRUDBase(HangerInfo)
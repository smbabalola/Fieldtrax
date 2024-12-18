# File: backend/app/crud/logisticssystem/crud_backload.py
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.logisticsystem.backload import Backload
from app.schemas.logisticsystem.backload import BackloadCreate, BackloadUpdate

class CRUDBackload(CRUDBase[Backload, BackloadCreate, BackloadUpdate]):
    async def get_by_wellbore(
        self, 
        db: Session, 
        *, 
        wellbore_id: str
    ) -> List[Backload]:
        """Get all backloads for a wellbore"""
        return db.query(Backload).filter(
            Backload.wellbore_id == wellbore_id
        ).order_by(Backload.date.desc()).all()

    async def get_by_sheet_number(
        self, 
        db: Session, 
        *, 
        sheet_number: str
    ) -> Optional[Backload]:
        """Get backload by sheet number"""
        return db.query(Backload).filter(
            Backload.sheet_number == sheet_number
        ).first()

    async def get_pending_approvals(
        self,
        db: Session,
        *,
        wellbore_id: Optional[str] = None
    ) -> List[Backload]:
        """Get backloads pending approval"""
        query = db.query(Backload).filter(Backload.approved_by.is_(None))
        if wellbore_id:
            query = query.filter(Backload.wellbore_id == wellbore_id)
        return query.order_by(Backload.date.desc()).all()

    async def approve_backload(
        self,
        db: Session,
        *,
        backload_id: str,
        approved_by: str
    ) -> Optional[Backload]:
        """Approve a backload"""
        backload = await self.get(db=db, id=backload_id)
        if backload:
            backload.approved_by = approved_by
            backload.status = "approved"
            db.add(backload)
            db.commit()
            db.refresh(backload)
        return backload

crud_backload = CRUDBackload(Backload)

# from app.models.logisticsystem.backload import Backload
# from app.crud.base import CRUDBase

# crud_backload = CRUDBase(Backload)
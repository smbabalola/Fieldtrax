# File: backend/app/crud/jobsystem/tally_item.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.tally_item import TallyItem
from app.schemas.jobsystem.tally_item import TallyItemCreate, TallyItemUpdate

class CRUDTallyItem(CRUDBase[TallyItem, TallyItemCreate, TallyItemUpdate]):
    async def get_by_tally(
        self,
        db: Session,
        *,
        tally_id: str
    ) -> List[TallyItem]:
        """Get all items for a tally"""
        return db.query(TallyItem).filter(
            TallyItem.tally_id == tally_id
        ).order_by(TallyItem.id).all()

    async def get_by_serial_number(
        self,
        db: Session,
        *,
        serial_number: str
    ) -> Optional[TallyItem]:
        """Get item by serial number"""
        return db.query(TallyItem).filter(
            TallyItem.serial_number == serial_number
        ).first()

    async def calculate_total_length(
        self,
        db: Session,
        *,
        tally_id: str
    ) -> float:
        """Calculate total length of tally items"""
        items = await self.get_by_tally(db=db, tally_id=tally_id)
        return sum(item.length_value for item in items)

crud_tally_item = CRUDTallyItem(TallyItem)

# from app.models.jobsystem.tally_item import TallyItem
# from app.crud.base import CRUDBase

# crud_tally_item = CRUDBase(TallyItem)
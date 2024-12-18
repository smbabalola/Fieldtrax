# File: backend/app/crud/jobsystem/tally.py
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.tally import Tally
from app.schemas.jobsystem.tally import TallyCreate, TallyUpdate

class CRUDTally(CRUDBase[Tally, TallyCreate, TallyUpdate]):
    async def get_by_wellbore(
        self,
        db: Session,
        *,
        wellbore_id: str
    ) -> List[Tally]:
        """Get all tallies for a wellbore"""
        return db.query(Tally).filter(
            Tally.wellbore_id == wellbore_id
        ).order_by(Tally.date.desc()).all()

    async def get_verified_tallies(
        self,
        db: Session,
        *,
        wellbore_id: str
    ) -> List[Tally]:
        """Get verified tallies"""
        return db.query(Tally).filter(
            Tally.wellbore_id == wellbore_id,
            Tally.verified_by.isnot(None)
        ).order_by(Tally.date.desc()).all()

    async def verify_tally(
        self,
        db: Session,
        *,
        tally_id: str,
        verified_by: str
    ) -> Optional[Tally]:
        """Mark tally as verified"""
        tally = await self.get(db=db, id=tally_id)
        if tally:
            tally.verified_by = verified_by
            db.add(tally)
            db.commit()
            db.refresh(tally)
        return tally

crud_tally = CRUDTally(Tally)


# from app.models.jobsystem.tally import Tally
# from app.crud.base import CRUDBase

# crud_tally = CRUDBase(Tally)
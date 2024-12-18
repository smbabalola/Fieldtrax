# File: backend/app/crud/jobsystem/crud_physical_barrier.py
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.physical_barrier import PhysicalBarrier
from app.schemas.jobsystem.physical_barrier import (
    PhysicalBarrierCreate, 
    PhysicalBarrierUpdate
)

class CRUDPhysicalBarrier(CRUDBase[PhysicalBarrier, PhysicalBarrierCreate, PhysicalBarrierUpdate]):
    async def get_by_wellbore(
        self, 
        db: Session, 
        *, 
        wellbore_id: str
    ) -> List[PhysicalBarrier]:
        """Get all physical barriers for a wellbore"""
        return db.query(PhysicalBarrier).filter(
            PhysicalBarrier.wellbore_id == wellbore_id
        ).order_by(PhysicalBarrier.depth_value).all()

    async def get_verified_barriers(
        self, 
        db: Session, 
        *, 
        wellbore_id: str
    ) -> List[PhysicalBarrier]:
        """Get all verified barriers"""
        return db.query(PhysicalBarrier).filter(
            PhysicalBarrier.wellbore_id == wellbore_id,
            PhysicalBarrier.verified_by.isnot(None)
        ).all()

    async def mark_verified(
        self,
        db: Session,
        *,
        barrier_id: str,
        verified_by: str
    ) -> Optional[PhysicalBarrier]:
        """Mark a barrier as verified"""
        barrier = await self.get(db=db, id=barrier_id)
        if barrier:
            barrier.verified_by = verified_by
            barrier.verification_date = datetime.utcnow()
            db.add(barrier)
            db.commit()
            db.refresh(barrier)
        return barrier

crud_physical_barrier = CRUDPhysicalBarrier(PhysicalBarrier)

# from app.models.jobsystem.physical_barrier import PhysicalBarrier
# from app.crud.base import CRUDBase

# crud_physical_barrier = CRUDBase(PhysicalBarrier)
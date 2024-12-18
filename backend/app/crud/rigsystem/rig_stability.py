# File: backend/app/crud/rigsystem/crud_rig_stability.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.rigsystem.rig_stability import RigStability
from app.schemas.rigsystem.rig_stability import RigStabilityCreate, RigStabilityUpdate

class CRUDRigStability(CRUDBase[RigStability, RigStabilityCreate, RigStabilityUpdate]):
    async def get_by_rig(
        self,
        db: Session,
        *,
        rig_id: str
    ) -> Optional[RigStability]:
        """Get stability data for a rig"""
        return db.query(RigStability).filter(
            RigStability.rig_id == rig_id
        ).first()

    async def get_rigs_by_capacity(
        self,
        db: Session,
        *,
        min_deck_load: float
    ) -> List[RigStability]:
        """Get rigs by minimum deck load capacity"""
        return db.query(RigStability).filter(
            RigStability.max_deck_load_op_draft >= min_deck_load
        ).all()

crud_rig_stability = CRUDRigStability(RigStability)

# from app.models.rigsystem.rig_stability import RigStability
# from app.crud.base import CRUDBase

# crud_rig_stability = CRUDBase(RigStability)
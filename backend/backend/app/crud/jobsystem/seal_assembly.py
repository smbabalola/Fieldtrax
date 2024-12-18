# File: backend/app//jobsystem/seal_assembly.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.mud_equipment_detail import MudEquipmentDetail
from app.models.jobsystem.seal_assembly import SealAssembly
from app.schemas.jobsystem.seal_assembly import (
    SealAssemblyCreate, 
    SealAssemblyUpdate
)

class CRUDSealAssembly(CRUDBase[SealAssembly, SealAssemblyCreate, SealAssemblyUpdate]):
    async def get_by_wellbore(
        self, 
        db: Session, 
        *, 
        wellbore_id: str
    ) -> List[SealAssembly]:
        """Get all seal assemblies for a wellbore"""
        return db.query(SealAssembly).filter(
            SealAssembly.wellbore_id == wellbore_id
        ).all()
# Create instances
crud_seal_assembly = CRUDSealAssembly(SealAssembly)

# from app.models.jobsystem.seal_assembly import SealAssembly
# from app.crud.base import CRUDBase

# crud_seal_assembly = CRUDBase(SealAssembly)
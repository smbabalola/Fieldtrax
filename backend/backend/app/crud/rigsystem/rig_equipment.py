# File: backend/app/crud/rigsystem/crud_rig_equipment.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.rigsystem.rig_equipment import RigEquipment
from app.schemas.rigsystem.rig_equipment import RigEquipmentCreate, RigEquipmentUpdate

class CRUDRigEquipment(CRUDBase[RigEquipment, RigEquipmentCreate, RigEquipmentUpdate]):
    async def get_by_rig(
        self,
        db: Session,
        *,
        rig_id: str
    ) -> Optional[RigEquipment]:
        """Get equipment for a rig"""
        return db.query(RigEquipment).filter(
            RigEquipment.rig_id == rig_id
        ).first()

    async def get_by_manufacturer(
        self,
        db: Session,
        *,
        manufacturer: str
    ) -> List[RigEquipment]:
        """Get equipment by manufacturer"""
        return db.query(RigEquipment).filter(
            RigEquipment.derrick_manufacturer == manufacturer
        ).all()

crud_rig_equipment = CRUDRigEquipment(RigEquipment)
# from app.models.rigsystem.rig_equipment import RigEquipment
# from app.crud.base import CRUDBase

# crud_rig_equipment = CRUDBase(RigEquipment)
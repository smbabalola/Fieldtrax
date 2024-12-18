# File: backend/app/crud/rigsystem/crud_rotary_equipment.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.rigsystem.rotary_equipment import RotaryEquipment
from app.schemas.rigsystem.rotary_equipment import RotaryEquipmentCreate, RotaryEquipmentUpdate

class CRUDRotaryEquipment(CRUDBase[RotaryEquipment, RotaryEquipmentCreate, RotaryEquipmentUpdate]):
    async def get_by_rig(
        self,
        db: Session,
        *,
        rig_id: str
    ) -> Optional[RotaryEquipment]:
        """Get rotary equipment for a rig"""
        return db.query(RotaryEquipment).filter(
            RotaryEquipment.rig_id == rig_id
        ).first()

    async def get_by_manufacturer(
        self,
        db: Session,
        *,
        manufacturer: str
    ) -> List[RotaryEquipment]:
        """Get equipment by top drive manufacturer"""
        return db.query(RotaryEquipment).filter(
            RotaryEquipment.top_drive_manufacturer == manufacturer
        ).all()

    async def get_by_power_rating(
        self,
        db: Session,
        *,
        min_power: float
    ) -> List[RotaryEquipment]:
        """Get equipment by minimum power rating"""
        return db.query(RotaryEquipment).filter(
            RotaryEquipment.top_drive_power_rating >= min_power
        ).all()

crud_rotary_equipment = CRUDRotaryEquipment(RotaryEquipment)

# from app.models.rigsystem.rotary_equipment import RotaryEquipment
# from app.crud.base import CRUDBase

# crud_rotary_equipment = CRUDBase(RotaryEquipment)
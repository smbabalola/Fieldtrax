# File: backend/app/crud/rigsystem/crud_well_control_equipment.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.rigsystem.well_control_equipment import WellControlEquipment
from app.schemas.rigsystem.well_control_equipment import (
    WellControlEquipmentCreate,
    WellControlEquipmentUpdate
)

class CRUDWellControlEquipment(CRUDBase[WellControlEquipment, WellControlEquipmentCreate, WellControlEquipmentUpdate]):
    async def get_by_rig(
        self,
        db: Session,
        *,
        rig_id: str
    ) -> Optional[WellControlEquipment]:
        """Get well control equipment for a rig"""
        return db.query(WellControlEquipment).filter(
            WellControlEquipment.rig_id == rig_id
        ).first()

    async def get_by_pressure_rating(
        self,
        db: Session,
        *,
        min_pressure: float
    ) -> List[WellControlEquipment]:
        """Get equipment by minimum pressure rating"""
        return db.query(WellControlEquipment).filter(
            WellControlEquipment.bop_max_pressure >= min_pressure
        ).all()

    async def get_by_manufacturer(
        self,
        db: Session,
        *,
        manufacturer: str
    ) -> List[WellControlEquipment]:
        """Get equipment by diverter manufacturer"""
        return db.query(WellControlEquipment).filter(
            WellControlEquipment.diverter_manufacturer == manufacturer
        ).all()

crud_well_control_equipment = CRUDWellControlEquipment(WellControlEquipment)

# from app.models.rigsystem.well_control_equipment import WellControlEquipment
# from app.crud.base import CRUDBase

# crud_well_control_equipment = CRUDBase(WellControlEquipment)
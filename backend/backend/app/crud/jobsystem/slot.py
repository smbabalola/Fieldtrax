# File: backend/app/crud/jobsystem/crud_slot.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.slot import Slot
from app.schemas.jobsystem.slot import SlotCreate, SlotUpdate

class CRUDSlot(CRUDBase[Slot, SlotCreate, SlotUpdate]):
    async def get_by_installation(
        self, 
        db: Session, 
        *, 
        installation_id: str
    ) -> List[Slot]:
        """
        Get all slots for a specific installation.
        """
        return db.query(Slot).filter(
            Slot.installation_id == installation_id
        ).all()

    async def get_by_slot_name(
        self, 
        db: Session, 
        *, 
        slot_name: str,
        installation_id: str
    ) -> Optional[Slot]:
        """
        Get slot by name within an installation.
        This allows for unique slot names per installation.
        """
        return db.query(Slot).filter(
            Slot.slot_name == slot_name,
            Slot.installation_id == installation_id
        ).first()

    async def get_slots_by_coordinates(
        self,
        db: Session,
        *,
        min_eastings: float,
        max_eastings: float,
        min_northings: float,
        max_northings: float
    ) -> List[Slot]:
        """
        Get slots within a coordinate boundary.
        Useful for mapping and spatial queries.
        """
        return db.query(Slot).filter(
            Slot.utm_eastings >= min_eastings,
            Slot.utm_eastings <= max_eastings,
            Slot.utm_northings >= min_northings,
            Slot.utm_northings <= max_northings
        ).all()

    async def get_slots_with_wells(
        self,
        db: Session,
        *,
        installation_id: str
    ) -> List[Slot]:
        """
        Get all slots that have associated wells.
        """
        return db.query(Slot).filter(
            Slot.installation_id == installation_id,
            Slot.wells.any()
        ).all()

    async def get_available_slots(
        self,
        db: Session,
        *,
        installation_id: str
    ) -> List[Slot]:
        """
        Get all slots that don't have any associated wells.
        Useful for planning new wells.
        """
        return db.query(Slot).filter(
            Slot.installation_id == installation_id,
            ~Slot.wells.any()
        ).all()

    async def update_coordinates(
        self,
        db: Session,
        *,
        slot_id: str,
        utm_eastings: float = None,
        utm_northings: float = None,
        latitude: str = None,
        longitude: str = None
    ) -> Optional[Slot]:
        """
        Update slot coordinates with validation.
        """
        slot = await self.get(db=db, id=slot_id)
        if not slot:
            return None

        if utm_eastings is not None:
            slot.utm_eastings = utm_eastings
        if utm_northings is not None:
            slot.utm_northings = utm_northings
        if latitude is not None:
            slot.latitude = latitude
        if longitude is not None:
            slot.longitude = longitude

        db.add(slot)
        db.commit()
        db.refresh(slot)
        return slot

    async def batch_create_slots(
        self,
        db: Session,
        *,
        installation_id: str,
        slot_names: List[str]
    ) -> List[Slot]:
        """
        Batch create multiple slots for an installation.
        Useful for initial installation setup.
        """
        slots = []
        for slot_name in slot_names:
            slot = Slot(
                installation_id=installation_id,
                slot_name=slot_name
            )
            db.add(slot)
            slots.append(slot)
        
        db.commit()
        for slot in slots:
            db.refresh(slot)
        return slots

    async def get_slot_statistics(
        self,
        db: Session,
        *,
        installation_id: str
    ) -> dict:
        """
        Get statistics about slots in an installation.
        Returns total slots, occupied slots, and available slots.
        """
        total_slots = await db.query(Slot).filter(
            Slot.installation_id == installation_id
        ).count()
        
        occupied_slots = await db.query(Slot).filter(
            Slot.installation_id == installation_id,
            Slot.wells.any()
        ).count()

        return {
            "total_slots": total_slots,
            "occupied_slots": occupied_slots,
            "available_slots": total_slots - occupied_slots
        }

# Create instance
crud_slot = CRUDSlot(Slot)

# from app.models.jobsystem.slot import Slot
# from app.crud.base import CRUDBase

# crud_slot = CRUDBase(Slot)
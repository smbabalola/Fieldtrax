# File: backend/app/crud/rigsystem/crud_mud_pump.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.rigsystem.mud_pump import MudPump
from app.schemas.rigsystem.mud_pump import MudPumpCreate, MudPumpUpdate

class CRUDMudPump(CRUDBase[MudPump, MudPumpCreate, MudPumpUpdate]):
    async def get_by_rig(
        self,
        db: Session,
        *,
        rig_id: str
    ) -> List[MudPump]:
        """Get all mud pumps for a rig"""
        return db.query(MudPump).filter(
            MudPump.rig_id == rig_id
        ).all()

    async def get_by_serial_number(
        self,
        db: Session,
        *,
        serial_number: str
    ) -> Optional[MudPump]:
        """Get mud pump by serial number"""
        return db.query(MudPump).filter(
            MudPump.serial_number == serial_number
        ).first()

    async def get_by_type(
        self,
        db: Session,
        *,
        pump_type: str,
        rig_id: Optional[str] = None
    ) -> List[MudPump]:
        """Get mud pumps by type"""
        query = db.query(MudPump).filter(MudPump.pump_type == pump_type)
        if rig_id:
            query = query.filter(MudPump.rig_id == rig_id)
        return query.all()
    
crud_mud_pump = CRUDMudPump(MudPump)
# from app.models.rigsystem.mud_pump import MudPump
# from app.crud.base import CRUDBase

# crud_mud_pump = CRUDBase(MudPump)
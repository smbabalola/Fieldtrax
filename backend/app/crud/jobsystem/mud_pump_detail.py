# File: backend/app/crud/jobsystem/crud_mud_pump_detail.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.mud_pump_detail import MudPumpDetail
from app.schemas.jobsystem.mud_pump_detail import MudPumpDetailCreate, MudPumpDetailUpdate

class CRUDMudPumpDetail(CRUDBase[MudPumpDetail, MudPumpDetailCreate, MudPumpDetailUpdate]):
    async def get_by_report(
        self, 
        db: Session, 
        *, 
        report_id: str
    ) -> List[MudPumpDetail]:
        """Get all mud pump details for a daily report"""
        return db.query(MudPumpDetail).filter(
            MudPumpDetail.report_id == report_id
        ).all()

    async def get_active_pumps(
        self, 
        db: Session, 
        *, 
        report_id: str
    ) -> List[MudPumpDetail]:
        """Get all active mud pumps for a report"""
        return db.query(MudPumpDetail).filter(
            MudPumpDetail.report_id == report_id,
            MudPumpDetail.for_hole == True
        ).all()

crud_mud_pump_detail = CRUDMudPumpDetail(MudPumpDetail)

# from app.models.jobsystem.mud_pump_detail import MudPumpDetail
# from app.crud.base import CRUDBase

# crud_mud_pump_detail = CRUDBase(MudPumpDetail)

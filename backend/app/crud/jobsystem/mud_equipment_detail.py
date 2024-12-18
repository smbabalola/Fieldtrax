from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.mud_equipment_detail import MudEquipmentDetail
from app.schemas.jobsystem.mud_equipment_detail import (
    MudEquipmentDetailCreate, 
    MudEquipmentDetailUpdate
)

class CRUDMudEquipmentDetail(CRUDBase[MudEquipmentDetail, MudEquipmentDetailCreate, MudEquipmentDetailUpdate]):
    async def get_by_report(
        self, 
        db: Session, 
        *, 
        report_id: str
    ) -> List[MudEquipmentDetail]:
        """Get all mud equipment details for a daily report"""
        return db.query(MudEquipmentDetail).filter(
            MudEquipmentDetail.report_id == report_id
        ).all()

    async def get_by_equipment(
        self, 
        db: Session, 
        *, 
        mud_equipment_id: str
    ) -> List[MudEquipmentDetail]:
        """Get all details for specific mud equipment"""
        return db.query(MudEquipmentDetail).filter(
            MudEquipmentDetail.mud_equipment_id == mud_equipment_id
        ).all()

crud_mud_equipment_detail = CRUDMudEquipmentDetail(MudEquipmentDetail)
# from app.models.jobsystem.mud_equipment_detail import MudEquipmentDetail
# from app.crud.base import CRUDBase

# crud_mud_equipment_detail = CRUDBase(MudEquipmentDetail)
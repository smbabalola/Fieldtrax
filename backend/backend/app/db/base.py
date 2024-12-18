# File: backend/app/db/base.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base
from app.db.sync_manager import record_change
from app.db.session import db_manager  # Add this import

from app.models.authsystem.user import User  # Add this import
from app.models.authsystem.user_session import UserSession  # Add this import
from app.models.authsystem.password_reset import PasswordReset  # Add this import

from app.models.jobsystem.job import Job  # Add this import
from app.models.jobsystem.daily_report import DailyReport  # Add this import
from app.models.jobsystem.field import Field  # Add this import
from app.models.jobsystem.fluid import Fluid  # Add this import 
from app.models.jobsystem.hanger_info import HangerInfo  # Add this import 
from app.models.jobsystem.installation_type import InstallationType  # Add this import 
from app.models.jobsystem.installation import Installation  # Add this import
from app.models.jobsystem.job_center import JobCenter  # Add this import
from app.models.jobsystem.job_log import JobLog  # Add this import
from app.models.jobsystem.job_parameter import JobParameter  # Add this import
from app.models.jobsystem.mud_equipment_detail import MudEquipmentDetail  # Add this import
from app.models.jobsystem.mud_pump_detail import MudPumpDetail  # Add this import
from app.models.jobsystem.operational_parameter import OperationalParameter  # Add this import
from app.models.jobsystem.operator import Operator  # Add this import
from app.models.jobsystem.physical_barrier import PhysicalBarrier  # Add this import
from app.models.jobsystem.production import Production  # Add this import
from app.models.jobsystem.seal_assembly import SealAssembly  # Add this import
from app.models.jobsystem.slot import Slot  # Add this import
from app.models.jobsystem.time_sheet import TimeSheet  # Add this import
from app.models.jobsystem.tally import Tally  # Add this import
from app.models.jobsystem.tally_item import TallyItem  # Add this import
from app.models.jobsystem.trajectory import Trajectory  # Add this import
from app.models.jobsystem.tubular import Tubular  # Add this import
from app.models.jobsystem.tubular_type import TubularType  # Add this import    
from app.models.jobsystem.well_shape import WellShape  # Add this import
from app.models.jobsystem.well import Well  # Add this import
from app.models.jobsystem.wellbore import Wellbore  # Add this import
from app.models.jobsystem.well_type import WellType  # Add this import
from app.models.rigsystem.contractor import Contractor  # Add this import

from app.models.logisticsystem.backload import Backload  # Add this import
from app.models.logisticsystem.contract_type import ContractType  # Add this import
from app.models.logisticsystem.delivery_ticket_item import DeliveryTicketItem  # Add this import
from app.models.logisticsystem.delivery_ticket import DeliveryTicket  # Add this import
from app.models.logisticsystem.purchase_order_item import PurchaseOrderItem  # Add this import
from app.models.logisticsystem.purchase_order import PurchaseOrder  # Add this import

from app.models.rigsystem.contractor import Contractor  # Add this import
from app.models.rigsystem.mud_equipment import MudEquipment  # Add this import
from app.models.rigsystem.mud_pump  import MudPump  # Add this import
from app.models.rigsystem.rig import Rig  # Add this import
from app.models.rigsystem.rig_equipment import RigEquipment  # Add this import
from app.models.rigsystem.rig_stability import RigStability  # Add this import
from app.models.rigsystem.tank import Tank # Add this import
from app.models.rigsystem.rig_equipment import RigEquipment  # Add this import
from app.models.rigsystem.well_control_equipment import WellControlEquipment  # Add this import

__all__ = [
    "Base",
    "User",
    "UserSession",
    "PasswordReset",
    "DailyReport",
    "Field",
    "Fluid",
    "HangerInfo",
    "InstallationType",
    "Installation",
    "JobCenter",
    "JobLog",
    "JobParameter",
    "Job",
    "MudEquipmentDetail",
    "MudPumpDetail",
    "OperationalParameter",
    "Operator",
    "PhysicalBarrier",
    "Production",
    "SealAssembly",
    "Slot",
    "TimeSheet",
    "Tally",
    "TallyItem",
    "Trajectory",
    "Tubular",
    "TubularType",
    "WellShape",
    "Well",
    "Wellbore",
    "WellType",
    "Wellshape",
    "WellboreGeometry",
    "backload",
    "ContractType",
    "DeliveryTicketItem",
    "DeliveryTicket",
    "PurchaseOrderItem",
    "PurchaseOrder",
    "Contractor",
    "MudEquipment",
    "MudPump",
    "Rig",
    "RigEquipment",
    "RigStability",
    "Tank",
    "RotaryEquipment",
    "WellControlEquipment",
]
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Record for sync when offline
        if not db_manager.is_online:
            record_change(
                table_name=self.model.__tablename__,
                operation='INSERT',
                data=obj_in_data
            )

        return db_obj

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True) if isinstance(obj_in, BaseModel) else obj_in

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Record for sync when offline
        if not db_manager.is_online:
            record_change(
                table_name=self.model.__tablename__,
                operation='UPDATE',
                data={
                    'id': db_obj.id,
                    **update_data
                }
            )

        return db_obj

    async def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()

        # Record for sync when offline
        if not db_manager.is_online:
            record_change(
                table_name=self.model.__tablename__,
                operation='DELETE',
                data={'id': id}
            )

        return obj
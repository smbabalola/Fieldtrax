# File: backend/app/db/base_all.py
"""
This module imports all models for Alembic autogeneration.
Use explicit imports instead of __init__.py to maintain clear dependencies.
"""

from app.db.base_class import Base

# Auth Models
from app.models.user import User
from app.models.user_session import UserSession
from app.models.password_reset import PasswordReset

# Well Models
from app.models.well import Well
from app.models.wellbore import Wellbore
from app.models.wellbore_geometry import WellboreGeometry
from app.models.well_shape import WellShape
from app.models.well_type import WellType
from app.models.trajectory import Trajectory

# Job Models
from app.models.job import Job
from app.models.job_center import JobCenter
from app.models.job_log import JobLog
from app.models.time_sheet import TimeSheet

# Equipment Models
from app.models.rig import Rig
from app.models.rig_equipment import RigEquipment
from app.models.rig_stability import RigStability
from app.models.rotary_equipment import RotaryEquipment
from app.models.well_control_equipment import WellControlEquipment
from app.models.tank import Tank
from app.models.mud_equipment import MudEquipment
from app.models.mud_equipment_detail import MudEquipmentDetail
from app.models.mud_pump import MudPump
from app.models.mud_pump_detail import MudPumpDetail

# Organization Models
from app.models.contractor import Contractor
from app.models.operator import Operator

# Location Models
from app.models.field import Field
from app.models.installation import Installation
from app.models.installation_type import InstallationType
from app.models.slot import Slot

# Technical Models
from app.models.tubular import Tubular
from app.models.tubular_type import TubularType
from app.models.seal_assembly import SealAssembly
from app.models.hanger_info import HangerInfo
from app.models.physical_barrier import PhysicalBarrier
from app.models.operational_parameter import OperationalParameter
from app.models.job_parameter import RunParameter
from app.models.fluid import Fluid

# Documentation Models
from app.models.daily_report import DailyReport
from app.models.tally import Tally
from app.models.tally_item import TallyItem
from app.models.backload import Backload
from app.models.delivery_ticket import DeliveryTicket
from app.models.delivery_ticket_item import DeliveryTicketItem
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_item import PurchaseOrderItem
from app.models.contract_type import ContractType
from app.models.production import Production

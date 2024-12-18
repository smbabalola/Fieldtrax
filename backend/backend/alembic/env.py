from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import app modules
from app.database import Base
#authsystem
from app.models.authsystem.authorization.permission import Permission
from app.models.authsystem.authorization.role import Role
from app.models.authsystem.user import User
from app.models.authsystem.userrole import user_roles
from app.models.authsystem.user_session import UserSession
from app.models.authsystem.password_reset import PasswordReset
#jobsystem
from app.models.jobsystem.daily_report import DailyReport
from app.models.jobsystem.field import Field
from app.models.jobsystem.fluid import Fluid
from app.models.jobsystem.hanger_info import HangerInfo
from app.models.jobsystem.installation_type import InstallationType
from app.models.jobsystem.installation import Installation
from app.models.jobsystem.job_center import JobCenter
from app.models.jobsystem.job_log import JobLog
from app.models.jobsystem.job_parameter import JobParameter
from app.models.jobsystem.job import Job
from app.models.jobsystem.mud_equipment_detail import MudEquipmentDetail
from app.models.jobsystem.mud_pump_detail import MudPumpDetail
from app.models.jobsystem.operational_parameter import OperationalParameter
from app.models.jobsystem.operator import Operator
from app.models.jobsystem.physical_barrier import PhysicalBarrier
from app.models.jobsystem.production import Production
from app.models.jobsystem.seal_assembly import SealAssembly
from app.models.jobsystem.slots import Slots
from app.models.jobsystem.tally_item import Tally_Item
from app.models.jobsystem.tally import Tally
from app.models.jobsystem.time_sheet import TimeSheet
from app.models.jobsystem.trajectory import Trajectory
from app.models.jobsystem.tubular_type import TubularType
from app.models.jobsystem.tubular import Tubular
from app.models.jobsystem.well_shape import WellShape
from app.models.jobsystem.well_type import WellType
from app.models.jobsystem.well import Well
from app.models.jobsystem.wellbore_geometry import WellboreGeometry
from app.models.jobsystem.wellbore import Wellbore


#logisticsystem
from app.models.logisticsystem.backload import Backload
from app.models.logisticsystem.contract_type import ContractType
from app.models.logisticsystem.delivery_ticket import DeliveryTicket
from app.models.logisticsystem.delivery_ticket_item import DeliveryTicketItem
from app.models.logisticsystem.purchase_order_item import PurchaseOrderItem
from app.models.logisticsystem.purchase_order import PurchaseOrder

from app.core.config import settings


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here

# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

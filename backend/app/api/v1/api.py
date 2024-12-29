# File: backend/app/api/v1/api.py
from fastapi import APIRouter

# Import Authentication System Routers
from app.api.v1.endpoints.auth import (
    user, user_session, password_reset
)

# Import Job System Routers
from app.api.v1.endpoints.job import (
    job, wellbore, daily_report, field, fluid, hanger_info,
    installation, job_center, operational_parameter, operator,
    physical_barrier, production, mud_equipment_detail,
    mud_pump_detail, trajectory, time_sheet, tally, tally_item,
    slot, seal_assembly, job_parameter, tubular, tubular_type, 
    well,well_shape, well_type, installation_type, settings,
    activity
)

# Import Rig System Routers
from app.api.v1.endpoints.rig import (
    rig, rig_equipment, rig_type, well_control_equipment, mud_pump,
    contractor, rotary_equipment
)

# Import Logistics System Routers
from app.api.v1.endpoints.logistic import (
    backload, delivery_ticket, purchase_order
)

# Create main API router
api_router = APIRouter()

# Include Authentication System Routers
# api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(user_session.router, tags=["authentication"])
api_router.include_router(password_reset.router, prefix="/auth/password-reset", tags=["authentication"])

# Include Job System Routers
api_router.include_router(job.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(wellbore.router, prefix="/wellbores", tags=["wellbores"])
api_router.include_router(daily_report.router, prefix="/daily-reports", tags=["daily-reports"])
api_router.include_router(field.router, prefix="/fields", tags=["fields"])
api_router.include_router(fluid.router, prefix="/fluids", tags=["fluids"])
api_router.include_router(hanger_info.router, prefix="/hanger-info", tags=["hanger-info"])
api_router.include_router(installation.router, prefix="/installations", tags=["installations"])
api_router.include_router(job_center.router, prefix="/job-centers", tags=["job-centers"])
api_router.include_router(operational_parameter.router, prefix="/operational-parameters", tags=["operational-parameters"])
api_router.include_router(operator.router, prefix="/operators", tags=["operators"])
api_router.include_router(physical_barrier.router, prefix="/physical-barriers", tags=["physical-barriers"])
api_router.include_router(production.router, prefix="/productions", tags=["productions"])
api_router.include_router(mud_pump_detail.router, prefix="/mud-pump-details", tags=["mud-pump-details"])
api_router.include_router(mud_equipment_detail.router, prefix="/mud-equipment-details", tags=["mud-equipment-details"])
api_router.include_router(trajectory.router, prefix="/trajectories", tags=["trajectories"])
api_router.include_router(time_sheet.router, prefix="/time-sheets", tags=["time-sheets"])
api_router.include_router(tally.router, prefix="/tallies", tags=["tallies"])
api_router.include_router(tally_item.router, prefix="/tally-items", tags=["tally-items"])
api_router.include_router(slot.router, prefix="/slots", tags=["slots"])
api_router.include_router(seal_assembly.router, prefix="/seal-assemblies", tags=["seal-assemblies"])
api_router.include_router(job_parameter.router, prefix="/job-parameters", tags=["job-parameters"])
api_router.include_router(tubular.router, prefix="/tubulars", tags=["tubulars"])
api_router.include_router(tubular_type.router, prefix="/tubular-types", tags=["tubular-types"])
api_router.include_router(well.router, prefix="/wells", tags=["wells"])
api_router.include_router(well_shape.router, prefix="/well-shapes", tags=["well-shapes"])
api_router.include_router(well_type.router, prefix="/well-types", tags=["well-types"])
api_router.include_router(installation_type.router, prefix="/installation-types", tags=["installation-types"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(activity.router, prefix="/activities", tags=["activities"])

# Include Rig System Routers
api_router.include_router(rig.router, prefix="/rigs", tags=["rigs"])
api_router.include_router(rig_equipment.router, prefix="/rig-equipment", tags=["rig-equipment"])
api_router.include_router(rig_type.router, prefix="/rig-types", tags=["rig-types"])
api_router.include_router(well_control_equipment.router, prefix="/well-control-equipment", tags=["well-control-equipment"])
api_router.include_router(mud_pump.router, prefix="/mud-pumps", tags=["mud-pumps"])
api_router.include_router(contractor.router, prefix="/contractors", tags=["contractors"])
api_router.include_router(rotary_equipment.router, prefix="/rotary-equipment", tags=["rotary-equipment"])

# Include Logistics System Routers
api_router.include_router(backload.router, prefix="/backloads", tags=["backloads"])
api_router.include_router(delivery_ticket.router, prefix="/delivery-tickets", tags=["delivery-tickets"])
api_router.include_router(purchase_order.router, prefix="/purchase-orders", tags=["purchase-orders"])
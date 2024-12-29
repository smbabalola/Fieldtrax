#backload_sheet.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BackloadSheetBase(BaseModel):
    wellbore_id: str
    sheet_number: str
    date: datetime
    destination: str
    total_weight_value: float
    total_weight_unit: Optional[str] = None
    transportation_details: Optional[str] = None
    status: Optional[str] = None
    approved_by: Optional[str] = None

class BackloadSheetCreate(BackloadSheetBase):
    pass

class BackloadSheetUpdate(BackloadSheetBase):
    pass

class BackloadSheet(BackloadSheetBase):
    id: str

    class Config:
        from_attributes = True
from pydantic import BaseModel
from typing import Optional

#contractor.py
class ContractorBase(BaseModel):
    contractor_name: str
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    post_code: Optional[str] = None
    zipcode: Optional[str] = None
    phone_no_1: Optional[str] = None
    phone_no_2: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

class ContractorCreate(ContractorBase):
    pass

class ContractorUpdate(ContractorBase):
    pass

class Contractor(ContractorBase):
    id: int

    class Config:
        from_attributes = True

#daily_report.py
from pydantic import BaseModel
from datetime import datetime

class DailyReportBase(BaseModel):
    wellbore_id: str
    report_date: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DailyReportCreate(DailyReportBase):
    pass

class DailyReportUpdate(DailyReportBase):
    pass

class DailyReport(DailyReportBase):
    id: str

    class Config:
        from_attributes = True
#fluid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FluidBase(BaseModel):
    wellbore_id: str
    fluid_type: str
    volume_value: float
    volume_unit: Optional[str] = None
    density_value: float
    density_unit: Optional[str] = None
    viscosity_value: Optional[float] = None
    viscosity_unit: Optional[str] = None
    description: Optional[str] = None
    timestamp: Optional[datetime] = None

class FluidCreate(FluidBase):
    pass

class FluidUpdate(FluidBase):
    pass

class Fluid(FluidBase):
    id: str

    class Config:
        from_attributes = True

#hanger_info
from pydantic import BaseModel
from typing import Optional

class HangerInfoBase(BaseModel):
    wellbore_id: Optional[str] = None
    type: Optional[str] = None
    burst_rating: Optional[float] = None
    tensile_rating: Optional[float] = None
    hanging_capacity: Optional[float] = None
    hydraulic_setting_pressure: Optional[float] = None

class HangerInfoCreate(HangerInfoBase):
    pass

class HangerInfoUpdate(HangerInfoBase):
    pass

class HangerInfo(HangerInfoBase):
    id: str

    class Config:
        from_attributes = True

#job
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobBase(BaseModel):
    jobcenter_id: Optional[str] = None
    well_name: str
    po_number: Optional[str] = None
    company_code: Optional[str] = None
    service_code: Optional[str] = None
    rig_id: Optional[str] = None
    country: str
    field: str
    measured_depth: Optional[float] = None
    total_vertical_depth: Optional[str] = None
    spud_date: datetime
    status: Optional[str] = None
    mobilization_date: Optional[datetime] = None
    demobilization_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    job_closed: Optional[bool] = None
    trainingfile: Optional[bool] = None

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    pass

class Job(JobBase):
    id: str

    class Config:
        from_attributes = True
#job_center
from pydantic import BaseModel
from typing import Optional

class JobCenterBase(BaseModel):
    slot_id: int
    well_name: str
    short_name: Optional[str] = None
    api_number: Optional[str] = None
    spud_date: Optional[datetime] = None
    well_class_id: int
    production_id: int
    well_shape_id: int
    utm_eastings: Optional[float] = None
    utm_northings: Optional[float] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    water_depth: Optional[float] = None
    district: Optional[str] = None
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    post_code: Optional[str] = None
    county: Optional[str] = None
    country: Optional[str] = None
    updated_by: Optional[int] = None
    date_last_updated: Optional[datetime] = None

class JobCenterCreate(JobCenterBase):
    pass

class JobCenterUpdate(JobCenterBase):
    pass

class JobCenter(JobCenterBase):
    id: str

    class Config:
        from_attributes = True

#job_log

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobLogBase(BaseModel):
    job_id: str
    timestamp: datetime
    activity_type: str
    description: Optional[str] = None
    duration: Optional[float] = None

class JobLogCreate(JobLogBase):
    pass

class JobLogUpdate(JobLogBase):
    pass

class JobLog(JobLogBase):
    id: str

    class Config:
        from_attributes = True

#mud_equipment
from pydantic import BaseModel
from typing import Optional

class MudEquipmentBase(BaseModel):
    rig_id: str
    equipment_name: Optional[str] = None
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None

class MudEquipmentCreate(MudEquipmentBase):
    pass

class MudEquipmentUpdate(MudEquipmentBase):
    pass

class MudEquipment(MudEquipmentBase):
    id: str

    class Config:
        from_attributes = True

#mud_equipment_detail
from pydantic import BaseModel
from typing import Optional

class MudEquipmentDetailBase(BaseModel):
    report_id: str
    mud_equipment_id: int
    hours_run: Optional[int] = None
    screen_sizes: Optional[str] = None
    active_volume_lost: Optional[float] = None
    reserve_volume_lost: Optional[float] = None
    other: Optional[float] = None

class MudEquipmentDetailCreate(MudEquipmentDetailBase):
    pass

class MudEquipmentDetailUpdate(MudEquipmentDetailBase):
    pass

class MudEquipmentDetail(MudEquipmentDetailBase):
    id: str

    class Config:
        from_attributes = True


#mud_pump
from pydantic import BaseModel
from typing import Optional

class MudPumpBase(BaseModel):
    rig_id: str
    serial_number: Optional[str] = None
    stroke_length: Optional[float] = None
    max_pressure: Optional[float] = None
    power_rating: Optional[float] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    efficiency: Optional[float] = None
    pump_type: Optional[str] = None

class MudPumpCreate(MudPumpBase):
    pass

class MudPumpUpdate(MudPumpBase):
    pass

class MudPump(MudPumpBase):
    id: str

    class Config:
        from_attributes = True

#mud_pump_detail
from pydantic import BaseModel
from typing import Optional

class MudPumpDetailBase(BaseModel):
    report_id: str
    mud_pump_id: int
    circulation_rate: float
    for_hole: bool

class MudPumpDetailCreate(MudPumpDetailBase):
    pass

class MudPumpDetailUpdate(MudPumpDetailBase):
    pass

class MudPumpDetail(MudPumpDetailBase):
    id: str

    class Config:
        from_attributes = True

#operational_parameters
from pydantic import BaseModel
from typing import Optional

class OperationalParametersBase(BaseModel):
    wellbore_id: Optional[str] = None
    zone: Optional[str] = None
    wiper_trip: Optional[bool] = None
    returns_running_liner: Optional[bool] = None
    reamed: Optional[int] = None
    liner_to_target: Optional[bool] = None
    ball_seat_function: Optional[bool] = None
    hanger_function: Optional[bool] = None
    overpull_after_release: Optional[bool] = None
    surface_equipment_function: Optional[bool] = None
    returns_cementing: Optional[bool] = None
    packer_function: Optional[bool] = None
    hanger_bearing_function: Optional[bool] = None
    plug_system_function: Optional[bool] = None
    mud_type: Optional[bool] = None
    lcm_mud: Optional[bool] = None
    lcm_conc: Optional[float] = None
    lcm_formulation: Optional[str] = None
    spacer_type: Optional[int] = None
    pdp_latch: Optional[bool] = None
    pdp_latch_at_calculated: Optional[bool] = None
    lwp_bump: Optional[bool] = None
    lwp_bump_at_calculated: Optional[bool] = None
    plug_bump_pressure: Optional[float] = None
    hrde_mech_released: Optional[bool] = None
    pbr_filled_with: Optional[int] = None
    reciprocate_string_during_cmt: Optional[bool] = None
    rotated_while_setting_packer: Optional[bool] = None
    h2s_present: Optional[bool] = None

class OperationalParametersCreate(OperationalParametersBase):
    pass

class OperationalParametersUpdate(OperationalParametersBase):
    pass

class OperationalParameters(OperationalParametersBase):

#password_reset
class PasswordResetBase(BaseModel):
    user_id: str
    token: str
    is_used: Optional[bool] = None
    created_at: Optional[datetime] = None
    expires_at: datetime

class PasswordResetCreate(PasswordResetBase):
    pass

class PasswordResetUpdate(PasswordResetBase):
    pass

class PasswordReset(PasswordResetBase):
    id: str

    class Config:
        from_attributes = True

#physical_barrier
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PhysicalBarrierBase(BaseModel):
    wellbore_id: str
    barrier_type: str
    depth_value: float
    depth_unit: Optional[str] = None
    length_value: Optional[float] = None
    length_unit: Optional[str] = None
    pressure_rating_value: float
    pressure_rating_unit: Optional[str] = None
    installation_date: datetime
    installed_by: str
    verified_by: Optional[str] = None
    verification_date: Optional[datetime] = None

class PhysicalBarrierCreate(PhysicalBarrierBase):
    pass

class PhysicalBarrierUpdate(PhysicalBarrierBase):
    pass

class PhysicalBarrier(PhysicalBarrierBase):
    id: str

    class Config:
        from_attributes = True

#rig
from pydantic import BaseModel
from typing import Optional

class RigBase(BaseModel):
    rig_name: str
    contractor_id: int
    contractor_name: str
    air_gap: float
    rig_type_id: int

class RigCreate(RigBase):
    pass

class RigUpdate(RigBase):
    pass

class Rig(RigBase):
    id: str

    class Config:
        from_attributes = True

#rig_equipment
from pydantic import BaseModel
from typing import Optional

class RigEquipmentBase(BaseModel):
    rig_id: str
    derrick_height: Optional[float] = None
    derrick_rating: Optional[float] = None
    derrick_manufacturer: Optional[str] = None
    rig_model: Optional[str] = None
    rig_power: Optional[float] = None
    travel_equipment_weight: Optional[float] = None
    kelly_manufacturer: Optional[str] = None
    kelly_type: Optional[str] = None
    kelly_length: Optional[float] = None
    kelly_weight: Optional[float] = None
    kelly_internal_diameter: Optional[float] = None
    surface_pipe_one_id: Optional[float] = None
    surface_pipe_one_length: Optional[float] = None
    surface_pipe_one_pressure_rating: Optional[float] = None
    surface_pipe_two_id: Optional[float] = None
    surface_pipe_two_length: Optional[float] = None
    surface_pipe_two_pressure_rating: Optional[float] = None
    stand_pipe_id: Optional[float] = None
    stand_pipe_length: Optional[float] = None
    stand_pipe_pressure_rating: Optional[float] = None
    kelly_hose_id: Optional[float] = None
    kelly_hose_length: Optional[float] = None
    kelly_hose_pressure_rating: Optional[float] = None

class RigEquipmentCreate(RigEquipmentBase):
    pass

class RigEquipmentUpdate(RigEquipmentBase):
    pass

class RigEquipment(RigEquipmentBase):
    id: str

    class Config:
        from_attributes = True

#rig_stability
from pydantic import BaseModel
from typing import Optional

class RigStabilityBase(BaseModel):
    rig_id: str
    max_deck_load_op_draft: Optional[float] = None
    max_deck_load_survival_draft: Optional[float] = None
    max_deck_load_transit_draft: Optional[float] = None
    max_deck_load_water_depth: Optional[float] = None
    number_thrusters: Optional[float] = None
    thruster_power: Optional[float] = None
    number_anchors: Optional[int] = None
    number_riser_tensioners: Optional[int] = None
    number_guideline_tensioners: Optional[int] = None

class RigStabilityCreate(RigStabilityBase):
    pass

class RigStabilityUpdate(RigStabilityBase):
    pass

class RigStability(RigStabilityBase):
    id: str

    class Config:
        from_attributes = True

#rotary_equipment
from pydantic import BaseModel
from typing import Optional

class RotaryEquipmentBase(BaseModel):
    rig_id: str
    top_drive_manufacturer: Optional[str] = None
    top_drive_model: Optional[str] = None
    top_drive_power_rating: Optional[float] = None
    top_drive_torque_rating: Optional[float] = None
    top_drive_weight: Optional[float] = None
    rotary_table_manufacturer: Optional[str] = None
    rotary_table_model: Optional[str] = None
    rotary_table_power_rating: Optional[float] = None
    rotary_table_torque_rating: Optional[float] = None

class RotaryEquipmentCreate(RotaryEquipmentBase):
    pass

class RotaryEquipmentUpdate(RotaryEquipmentBase):
    pass

class RotaryEquipment(RotaryEquipmentBase):
    id: str

    class Config:
        from_attributes = True

#job_parameter
from pydantic import BaseModel
from typing import Optional

class RunParameterBase(BaseModel):
    wellbore_id: Optional[str] = None
    wiper_plug_pressure_rating: Optional[float] = None
    wiper_plug_temperature_rating: Optional[float] = None
    setting_tool_tensile: Optional[float] = None
    bumper_jar_tensile: Optional[float] = None
    surface_equipment_tensile: Optional[float] = None
    pickup_dogs: Optional[float] = None
    pickup_pack_off: Optional[float] = None
    shear_hrde_mech_release: Optional[float] = None
    make_up_torque_weak_link: Optional[float] = None
    weight_applied_packer_test: Optional[float] = None
    liner_top_deviation: Optional[float] = None
    ball_seat_type: Optional[str] = None
    pack_off_type: Optional[int] = None

class RunParameterCreate(RunParameterBase):
    pass

class RunParameterUpdate(RunParameterBase):
    pass

class RunParameter(RunParameterBase):
    id: str

    class Config:
        from_attributes = True

#seal_assembly
from pydantic import BaseModel
from typing import Optional

class SealAssemblyBase(BaseModel):
    wellbore_id: Optional[str] = None
    seal_surface_od: Optional[float] = None
    body_burst: Optional[float] = None
    collapse: Optional[float] = None
    tensile: Optional[float] = None
    tieback_extension_id: Optional[float] = None
    tieback_extension_burst: Optional[float] = None
    tieback_extension_collapse: Optional[float] = None
    tieback_yield_collapse: Optional[float] = None
    setting_force: Optional[float] = None
    hold_down_slips: Optional[bool] = None
    element_rating: Optional[float] = None
    slick_stinger_od: Optional[float] = None

class SealAssemblyCreate(SealAssemblyBase):
    pass

class SealAssemblyUpdate(SealAssemblyBase):
    pass

class SealAssembly(SealAssemblyBase):
    id: str

    class Config:
        from_attributes = True

#tally
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TallyBase(BaseModel):
    wellbore_id: str
    tally_type: str
    date: datetime
    total_length_value: float
    total_length_unit: Optional[str] = None
    total_weight_value: float
    total_weight_unit: Optional[str] = None
    created_by: str
    verified_by: Optional[str] = None

class TallyCreate(TallyBase):
    pass

class TallyUpdate(TallyBase):
    pass

class Tally(TallyBase):
    id: str

    class Config:
        from_attributes = True


#tally_item
from pydantic import BaseModel
from typing import Optional

class TallyItemBase(BaseModel):
    tally_id: str
    length_value: float
    length_unit: Optional[str] = None
    outer_diameter_value: float
    outer_diameter_unit: Optional[str] = None
    inner_diameter_value: Optional[float] = None
    inner_diameter_unit: Optional[str] = None
    weight_per_unit_value: float
    weight_per_unit_unit: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None

class TallyItemCreate(TallyItemBase):
    pass

class TallyItemUpdate(TallyItemBase):
    pass

class TallyItem(TallyItemBase):
    id: str

    class Config:
        from_attributes = True


#tank
from pydantic import BaseModel
from typing import Optional

class TankBase(BaseModel):
    rig_id: int
    tank_name: Optional[str] = None
    capacity: Optional[float] = None
    shape: Optional[str] = None
    length: Optional[float] = None
    height: Optional[float] = None
    width_top: Optional[float] = None
    width_bottom: Optional[float] = None

class TankCreate(TankBase):
    pass

class TankUpdate(TankBase):
    pass

class Tank(TankBase):
    id: int

    class Config:
        from_attributes = True

#time_sheet
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TimeSheetBase(BaseModel):
    wellbore_id: str
    employee_id: str
    date: datetime
    hours_worked: float
    activity_code: str
    description: Optional[str] = None
    approved: Optional[bool] = None
    approved_by: Optional[str] = None
    approval_date: Optional[datetime] = None

class TimeSheetCreate(TimeSheetBase):
    pass

class TimeSheetUpdate(TimeSheetBase):
    pass

class TimeSheet(TimeSheetBase):
    id: str

    class Config:
        from_attributes = True

#trajectory
from pydantic import BaseModel

class TrajectoryBase(BaseModel):
    wellbore_id: str
    measured_depth: float
    inclination: float
    azimuth: float

class TrajectoryCreate(TrajectoryBase):
    pass

class TrajectoryUpdate(TrajectoryBase):
    pass

class Trajectory(TrajectoryBase):
    id: str

    class Config:
        from_attributes = True


#tubular
from pydantic import BaseModel
from typing import Optional

class TubularBase(BaseModel):
    tubulartype_id: str
    outer_diameter: Optional[float] = None
    inner_diameter: Optional[float] = None
    weight: Optional[float] = None
    yield_strength: Optional[float] = None
    capacity: Optional[float] = None
    volume: Optional[float] = None
    thread: Optional[str] = None
    burst: Optional[float] = None
    collapse: Optional[float] = None
    drift: Optional[float] = None
    oh_diameter: Optional[float] = None
    liner_Overlap: Optional[float] = None
    start_depth: Optional[float] = None
    end_depth: Optional[float] = None
    liner_top_depth: Optional[str] = None

class TubularCreate(TubularBase):
    pass

class TubularUpdate(TubularBase):
    pass

class Tubular(TubularBase):
    id: str

    class Config:
        from_attributes = True


#tubularType
from pydantic import BaseModel
from typing import Optional

class TubularTypeBase(BaseModel):
    type: Optional[str] = None
    type_short: Optional[str] = None
    description: Optional[str] = None

class TubularTypeCreate(TubularTypeBase):
    pass

class TubularTypeUpdate(TubularTypeBase):
    pass

class TubularType(TubularTypeBase):
    id: str

    class Config:
        from_attributes = True

#user
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    hashed_password: str
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    verification_token: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: str

    class Config:
        from_attributes = True

#user_session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSessionBase(BaseModel):
    user_id: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: datetime
    created_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    is_active: Optional[bool] = None
    device_info: Optional[str] = None
    ip_address: Optional[str] = None

class UserSessionCreate(UserSessionBase):
    pass

class UserSessionUpdate(UserSessionBase):
    pass

class UserSession(UserSessionBase):
    id: str

    class Config:
        from_attributes = True

#well_control_Equipment
from pydantic import BaseModel
from typing import Optional

class WellControlEquipmentBase(BaseModel):
    rig_id: str
    choke_line_diameter: Optional[float] = None
    choke_line_pressure: Optional[float] = None
    kill_line_diameter: Optional[float] = None
    bop_size: Optional[float] = None
    bop_max_pressure: Optional[float] = None
    bop_max_temperature: Optional[float] = None
    diverter_manufacturer: Optional[str] = None
    diverter_model: Optional[str] = None
    line_number: Optional[int] = None
    internal_diameter: Optional[float] = None
    max_pressure: Optional[float] = None
    line_length: Optional[float] = None
    closing_time: Optional[float] = None

class WellControlEquipmentCreate(WellControlEquipmentBase):
    pass

class WellControlEquipmentUpdate(WellControlEquipmentBase):
    pass

class WellControlEquipment(WellControlEquipmentBase):
    id: str

    class Config:
        from_attributes = True


#wellbore
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WellboreBase(BaseModel):
    job_id: str
    short_name: str
    wellbore_name: str
    wellbore_number: Optional[str] = None
    contract_type_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    primary_currency: Optional[str] = None
    secondary_currency: Optional[str] = None
    planned_start_date: Optional[datetime] = None
    Planned_days: Optional[int] = None
    Planned_well_cost: Optional[float] = None
    actual_well_cost: Optional[float] = None

class WellboreCreate(WellboreBase):
    pass

class WellboreUpdate(WellboreBase):
    pass

class Wellbore(WellboreBase):
    id: str

    class Config:
        from_attributes = True

#wellbore_geometry
from pydantic import BaseModel

class WellboreGeometryBase(BaseModel):
    wellbore_id: str
    tubular_id: str

class WellboreGeometryCreate(WellboreGeometryBase):
    pass

class WellboreGeometryUpdate(WellboreGeometryBase):
    pass

class WellboreGeometry(WellboreGeometryBase):
    id: str

    class Config:
        from_attributes = True

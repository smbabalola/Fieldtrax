#backload.py
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class BackloadSheet(Base):
    __tablename__ = 'backload_sheet'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    wellbore_id = Column(String(50), ForeignKey('Wellbore.id'), nullable=False)
    sheet_number = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)
    destination = Column(String(50), nullable=False)
    total_weight_value = Column(Float, nullable=False)
    total_weight_unit = Column(String(50), nullable=True)
    transportation_details = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)
    approved_by = Column(String(50), nullable=True)

    # relationship
    wellbore = relationship('Wellbore', back_populates='backload_sheets')

#contractor.py
from sqlalchemy import Column, Integer, String, NCHAR
from app.database import Base

class Contractor(Base):
    __tablename__ = 'contractor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contractor_name = Column(String(30), nullable=False)
    address_1 = Column(String(30), nullable=True)
    address_2 = Column(String(30), nullable=True)
    post_code = Column(NCHAR(15), nullable=True)
    zipcode = Column(NCHAR(15), nullable=True)
    phone_no_1 = Column(String(15), nullable=True)
    phone_no_2 = Column(String(15), nullable=True)
    state = Column(NCHAR(30), nullable=True)
    country = Column(NCHAR(30), nullable=True)

#daily_report.py
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class DailyReport(Base):
    __tablename__ = 'daily_report'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    wellbore_id = Column(String(50), ForeignKey('Wellbore.id'), nullable=False)
    report_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # relationship
    wellbore = relationship('Wellbore', back_populates='daily_reports')

#fluid

from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Fluid(Base):
    __tablename__ = 'fluid'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    wellbore_id = Column(String(50), ForeignKey('Wellbore.id'), nullable=False)
    fluid_type = Column(String(50), nullable=False)
    volume_value = Column(Float, nullable=False)
    volume_unit = Column(String(30), nullable=True)
    density_value = Column(Float, nullable=False)
    density_unit = Column(String(30), nullable=True)
    viscosity_value = Column(Float, nullable=True)
    viscosity_unit = Column(String(30), nullable=True)
    description = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=True)

    # relationship
    wellbore = relationship('Wellbore', back_populates='fluids')

#hanger_info
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class HangerInfo(Base):
    __tablename__ = 'hanger_info'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    wellbore_id = Column(String(50), ForeignKey('Wellbore.id'), nullable=True)
    type = Column(String(20), nullable=True)
    burst_rating = Column(Float, nullable=True)
    tensile_rating = Column(Float, nullable=True)
    hanging_capacity = Column(Float, nullable=True)
    hydraulic_setting_pressure = Column(Float, nullable=True)

    # relationship
    wellbore = relationship('Wellbore', back_populates='hanger_infos')

#job
from sqlalchemy import Column, String, DateTime, Float, NCHAR, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def utcnow():
    return datetime.now(timezone.utc)

class Job(Base):
    __tablename__ = 'job'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    jobcenter_id = Column(String(50), ForeignKey('job_center.id'), nullable=True)
    well_name = Column(String(50), nullable=False)
    po_number = Column(String(50), nullable=True)
    company_code = Column(NCHAR(3), nullable=True)
    service_code = Column(NCHAR(4), nullable=True)
    rig_id = Column(String(50), nullable=True)
    country = Column(String(50), nullable=False)
    field = Column(String(50), nullable=False)
    measured_depth = Column(Float, nullable=True)
    total_vertical_depth = Column(NCHAR(10), nullable=True)
    spud_date = Column(DateTime, nullable=False)
    status = Column(String(30), nullable=True)
    mobilization_date = Column(DateTime, nullable=True)
    demobilization_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utcnow, nullable=True)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=True)
    job_closed = Column(Boolean, nullable=True)
    trainingfile = Column(Boolean, nullable=True)

    # Relationships
    job_center = relationship('JobCenter', back_populates='jobs')
    wellbores = relationship('Wellbore', back_populates='job')
    time_sheets = relationship('TimeSheet', back_populates='job')
    physical_barriers = relationship('PhysicalBarrier', back_populates='job')
    rig = relationship('Rig', back_populates='jobs')
    user_sessions = relationship('UserSession', back_populates='job')

    def __repr__(self):
        return f"<Job {self.id}>"

#job_center

from sqlalchemy import Column, String, Integer, Float, DateTime
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class JobCenter(Base):
    __tablename__ = 'job_center'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    slot_id = Column(Integer, nullable=False)
    well_name = Column(String(25), nullable=False)
    short_name = Column(String(10), nullable=True)
    api_number = Column(String(25), nullable=True)
    spud_date = Column(DateTime, nullable=True)
    well_class_id = Column(Integer, nullable=False)
    production_id = Column(Integer, nullable=False)
    well_shape_id = Column(Integer, nullable=False)
    utm_eastings = Column(Float, nullable=True)
    utm_northings = Column(Float, nullable=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    water_depth = Column(Float, nullable=True)
    district = Column(String(20), nullable=True)
    address_1 = Column(String(50), nullable=True)
    address_2 = Column(String(50), nullable=True)
    post_code = Column(String(8), nullable=True)
    county = Column(String(30), nullable=True)
    country = Column(String(30), nullable=True)
    updated_by = Column(Integer, nullable=True)
    date_last_updated = Column(DateTime, nullable=True)

    # Relationships
    jobs = relationship('Job', back_populates='job_center')

#job_log
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class JobLog(Base):
    __tablename__ = 'job_log'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    job_id = Column(String(50), ForeignKey('job.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    activity_type = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    duration = Column(Float, nullable=True)

    # relationship
    job = relationship('Job', back_populates='job_logs')

#mud_equipment
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class MudEquipment(Base):
    __tablename__ = 'mud_equipment'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    rig_id = Column(String(50), ForeignKey('rig.id'), nullable=False)
    equipment_name = Column(String(25), nullable=True)
    serial_number = Column(String(25), nullable=True)
    manufacturer = Column(String(25), nullable=True)
    model = Column(String(25), nullable=True)

    # relationship
    rig = relationship('Rig', back_populates='mud_equipments')

#mud_equipment_detail
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class MudEquipmentDetail(Base):
    __tablename__ = 'mud_equipment_detail'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    report_id = Column(String(50), ForeignKey('daily_report.id'), nullable=False)
    mud_equipment_id = Column(Integer, nullable=False)
    hours_run = Column(Integer, nullable=True)
    screen_sizes = Column(String(25), nullable=True)
    active_volume_lost = Column(Float, nullable=True)
    reserve_volume_lost = Column(Float, nullable=True)
    other = Column(Float, nullable=True)
    
    # Relationships
    daily_report = relationship('DailyReport', back_populates='mud_equipment_details')

#mud_pump
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class MudPump(Base):
    __tablename__ = 'mud_pump'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    rig_id = Column(String(50), ForeignKey('rig.id'), nullable=False)
    serial_number = Column(String(25), nullable=True)
    stroke_length = Column(Float, nullable=True)
    max_pressure = Column(Float, nullable=True)
    power_rating = Column(Float, nullable=True)
    manufacturer = Column(String(25), nullable=True)
    model = Column(String(25), nullable=True)
    efficiency = Column(Float, nullable=True)
    pump_type = Column(String(25), nullable=True)

    # Relationships
    rig = relationship('Rig', back_populates='mud_pumps')

#mud_pump_detail
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class MudPumpDetail(Base):
    __tablename__ = 'mud_pump_detail'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    report_id = Column(String(50), ForeignKey('daily_report.id'), nullable=False)
    mud_pump_id = Column(Integer, nullable=False)
    circulation_rate = Column(Float, nullable=False)
    for_hole = Column(Boolean, nullable=False)

    # Relationships
    daily_report = relationship('DailyReport', back_populates='mud_pump_details')

#operational_parameters
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, Text
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class OperationalParameters(Base):
    __tablename__ = 'operational_parameters'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    wellbore_id = Column(String(50), ForeignKey('Wellbore.id'), nullable=True)
    zone = Column(String(30), nullable=True)
    wiper_trip = Column(Boolean, nullable=True)
    returns_running_liner = Column(Boolean, nullable=True)
    reamed = Column(Integer, nullable=True)
    liner_to_target = Column(Boolean, nullable=True)
    ball_seat_function = Column(Boolean, nullable=True)
    hanger_function = Column(Boolean, nullable=True)
    overpull_after_release = Column(Boolean, nullable=True)
    surface_equipment_function = Column(Boolean, nullable=True)
    returns_cementing = Column(Boolean, nullable=True)
    packer_function = Column(Boolean, nullable=True)
    hanger_bearing_function = Column(Boolean, nullable=True)
    plug_system_function = Column(Boolean, nullable=True)
    mud_type = Column(Boolean, nullable=True)
    lcm_mud = Column(Boolean, nullable=True)
    lcm_conc = Column(Float, nullable=True)
    lcm_formulation = Column(Text, nullable=True)
    spacer_type = Column(Integer, nullable=True)
    pdp_latch = Column(Boolean, nullable=True)
    pdp_latch_at_calculated = Column(Boolean, nullable=True)
    lwp_bump = Column(Boolean, nullable=True)
    lwp_bump_at_calculated = Column(Boolean, nullable=True)
    plug_bump_pressure = Column(Float, nullable=True)
    hrde_mech_released = Column(Boolean, nullable=True)
    pbr_filled_with = Column(Integer, nullable=True)
    reciprocate_string_during_cmt = Column(Boolean, nullable=True)
    rotated_while_setting_packer = Column(Boolean, nullable=True)
    h2s_present = Column(Boolean, nullable=True)

    # Relationships
    wellbore = relationship('Wellbore', back_populates='operational_parameters')

#password_reset
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def utcnow():
    return datetime.now(timezone.utc)

class PasswordReset(Base):
    __tablename__ = 'password_reset'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    user_id = Column(String(50), ForeignKey('user.id'), nullable=False)
    token = Column(String(50), unique=True, nullable=False)
    is_used = Column(Boolean, nullable=True, default=False)
    created_at = Column(DateTime, default=utcnow, nullable=True)
    expires_at = Column(DateTime, nullable=False)

    # relationship
    user = relationship('User', back_populates='password_resets')

#physical_barrier
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class PhysicalBarrier(Base):
    __tablename__ = 'physical_barrier'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    wellbore_id = Column(String(50), ForeignKey('Wellbore.id'), nullable=False)
    barrier_type = Column(String(50), nullable=False)
    depth_value = Column(Float, nullable=False)
    depth_unit = Column(String(50), nullable=True)
    length_value = Column(Float, nullable=True)
    length_unit = Column(String(50), nullable=True)
    pressure_rating_value = Column(Float, nullable=False)
    pressure_rating_unit = Column(String(50), nullable=True)
    installation_date = Column(DateTime, nullable=False)
    installed_by = Column(String(50), nullable=False)
    verified_by = Column(String(50), nullable=True)
    verification_date = Column(DateTime, nullable=True)

    # relationship
    wellbore = relationship('Wellbore', back_populates='physical_barriers')

#rig
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Rig(Base):
    __tablename__ = 'rig'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    rig_name = Column(String(25), nullable=False)
    contractor_id = Column(Integer, ForeignKey('contractor.id'), nullable=False)
    contractor_name = Column(String(25), nullable=False)
    air_gap = Column(Float, nullable=False)
    rig_type_id = Column(Integer, nullable=False)

    # Relationships
    contractor = relationship('Contractor', back_populates='rigs')
    mud_equipments = relationship('MudEquipment', back_populates='rig')
    mud_pumps = relationship('MudPump', back_populates='rig')
    well_control_equipments = relationship('WellControlEquipment', back_populates='rig')

    def __repr__(self):
        return f"<Rig {self.id}>"

#rig_equipment
from sqlalchemy import Column, String, Float, ForeignKey
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class RigEquipment(Base):
    __tablename__ = 'rig_equipment'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    rig_id = Column(String(50), ForeignKey('rig.id'), nullable=False)
    derrick_height = Column(Float, nullable=True)
    derrick_rating = Column(Float, nullable=True)
    derrick_manufacturer = Column(String(25), nullable=True)
    rig_model = Column(String(25), nullable=True)
    rig_power = Column(Float, nullable=True)
    travel_equipment_weight = Column(Float, nullable=True)
    kelly_manufacturer = Column(String(25), nullable=True)
    kelly_type = Column(String(25), nullable=True)
    kelly_length = Column(Float, nullable=True)
    kelly_weight = Column(Float, nullable=True)
    kelly_internal_diameter = Column(Float, nullable=True)
    surface_pipe_one_id = Column(Float, nullable=True)
    surface_pipe_one_length = Column(Float, nullable=True)
    surface_pipe_one_pressure_rating = Column(Float, nullable=True)
    surface_pipe_two_id = Column(Float, nullable=True)
    surface_pipe_two_length = Column(Float, nullable=True)
    surface_pipe_two_pressure_rating = Column(Float, nullable=True)
    stand_pipe_id = Column(Float, nullable=True)
    stand_pipe_length = Column(Float, nullable=True)
    stand_pipe_pressure_rating = Column(Float, nullable=True)
    kelly_hose_id = Column(Float, nullable=True)
    kelly_hose_length = Column(Float, nullable=True)
    kelly_hose_pressure_rating = Column(Float, nullable=True)

    # Relationships
    rig = relationship('Rig', back_populates='rig_equipments')

#rig_stability
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class RigStability(Base):
    __tablename__ = 'rig_stability'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    rig_id = Column(String(50), ForeignKey('rig.id'), nullable=False)
    max_deck_load_op_draft = Column(Float, nullable=True)
    max_deck_load_survival_draft = Column(Float, nullable=True)
    max_deck_load_transit_draft = Column(Float, nullable=True)
    max_deck_load_water_depth = Column(Float, nullable=True)
    number_thrusters = Column(Float, nullable=True)
    thruster_power = Column(Float, nullable=True)
    number_anchors = Column(Integer, nullable=True)
    number_riser_tensioners = Column(Integer, nullable=True)
    number_guideline_tensioners = Column(Integer, nullable=True)

    # Relationships
    rig = relationship('Rig', back_populates='rig_stabilities')

#rotary_equipment
from sqlalchemy import Column, String, Float, ForeignKey
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class RotaryEquipment(Base):
    __tablename__ = 'rotary_equipment'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    rig_id = Column(String(50), ForeignKey('rig.id'), nullable=False)
    top_drive_manufacturer = Column(String(25), nullable=True)
    top_drive_model = Column(String(25), nullable=True)
    top_drive_power_rating = Column(Float, nullable=True)
    top_drive_torque_rating = Column(Float, nullable=True)
    top_drive_weight = Column(Float, nullable=True)
    rotary_table_manufacturer = Column(String(25), nullable=True)
    rotary_table_model = Column(String(25), nullable=True)
    rotary_table_power_rating = Column(Float, nullable=True)
    rotary_table_torque_rating = Column(Float, nullable=True)

    # Relationships
    rig = relationship('Rig', back_populates='rotary_equipments')

#job_parameter
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class RunParameter(Base):
    __tablename__ = 'job_parameters'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    wellbore_id = Column(String(50), ForeignKey('Wellbore.id'), nullable=True)
    wiper_plug_pressure_rating = Column(Float, nullable=True)
    wiper_plug_temperature_rating = Column(Float, nullable=True)
    setting_tool_tensile = Column(Float, nullable=True)
    bumper_jar_tensile = Column(Float, nullable=True)
    surface_equipment_tensile = Column(Float, nullable=True)
    pickup_dogs = Column(Float, nullable=True)
    pickup_pack_off = Column(Float, nullable=True)
    shear_hrde_mech_release = Column(Float, nullable=True)
    make_up_torque_weak_link = Column(Float, nullable=True)
    weight_applied_packer_test = Column(Float, nullable=True)
    liner_top_deviation = Column(Float, nullable=True)
    ball_seat_type = Column(String(10), nullable=True)
    pack_off_type = Column(Integer, nullable=True)

    # relationship
    wellbore = relationship('Wellbore', back_populates='job_parameters')


#seal_assembly
from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class SealAssembly(Base):
    __tablename__ = 'seal_assembly'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    wellbore_id = Column(String(50), ForeignKey('Wellbore.id'), nullable=True)
    seal_surface_od = Column(Float, nullable=True)
    body_burst = Column(Float, nullable=True)
    collapse = Column(Float, nullable=True)
    tensile = Column(Float, nullable=True)
    tieback_extension_id = Column(Float, nullable=True)
    tieback_extension_burst = Column(Float, nullable=True)
    tieback_extension_collapse = Column(Float, nullable=True)
    tieback_yield_collapse = Column(Float, nullable=True)
    setting_force = Column(Float, nullable=True)
    hold_down_slips = Column(Boolean, nullable=True)
    element_rating = Column(Float, nullable=True)
    slick_stinger_od = Column(Float, nullable=True)

    # relationship
    wellbore = relationship('Wellbore', back_populates='seal_assemblies')

#tally
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Tally(Base):
    __tablename__ = 'tally'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    wellbore_id = Column(String(50), ForeignKey('Wellbore.id'), nullable=False)
    tally_type = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)
    total_length_value = Column(Float, nullable=False)
    total_length_unit = Column(String(50), nullable=True)
    total_weight_value = Column(Float, nullable=False)
    total_weight_unit = Column(String(50), nullable=True)
    created_by = Column(String(50), nullable=False)
    verified_by = Column(String(50), nullable=True)

    # Relationships
    wellbore = relationship('Wellbore', back_populates='tallies')
    tally_items = relationship('TallyItem', back_populates='tally')

#tally_item
from sqlalchemy import Column, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class TallyItem(Base):
    __tablename__ = 'tally_item'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    tally_id = Column(String(50), ForeignKey('tally.id'), nullable=False)
    length_value = Column(Float, nullable=False)
    length_unit = Column(String(50), nullable=True)
    outer_diameter_value = Column(Float, nullable=False)
    outer_diameter_unit = Column(String(50), nullable=True)
    inner_diameter_value = Column(Float, nullable=True)
    inner_diameter_unit = Column(String(50), nullable=True)
    weight_per_unit_value = Column(Float, nullable=False)
    weight_per_unit_unit = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    serial_number = Column(String(50), nullable=True)

    # Relationships
    tally = relationship('Tally', back_populates='tally_items')

#tank
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from app.database import Base

class Tank(Base):
    __tablename__ = 'tank'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rig_id = Column(Integer, ForeignKey('rig.id'), nullable=False)
    tank_name = Column(String(10), nullable=True)
    capacity = Column(Float, nullable=True)
    shape = Column(String(20), nullable=True)
    length = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    width_top = Column(Float, nullable=True)
    width_bottom = Column(Float, nullable=True)

    # Relationships
    rig = relationship('Rig', back_populates='tanks')

#time_sheet
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class TimeSheet(Base):
    __tablename__ = 'time_sheet'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    wellbore_id = Column(String(50), ForeignKey('Wellbore.id'), nullable=False)
    employee_id = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)
    hours_worked = Column(Float, nullable=False)
    activity_code = Column(String(1), nullable=False)
    description = Column(Text, nullable=True)
    approved = Column(Boolean, nullable=True)
    approved_by = Column(String(50), nullable=True)
    approval_date = Column(DateTime, nullable=True)

    # Relationships
    wellbore = relationship('Wellbore', back_populates='time_sheets')


#trajectory
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Trajectory(Base):
    __tablename__ = 'trajectory'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    wellbore_id = Column(String(50), ForeignKey('Wellbore.id'), nullable=False)
    measured_depth = Column(Float, nullable=False)
    inclination = Column(Float, nullable=False)
    azimuth = Column(Float, nullable=False)

    # Relationships
    wellbore = relationship('Wellbore', back_populates='trajectories')


#tubular
from sqlalchemy import Column, String, Float, ForeignKey, NCHAR
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Tubular(Base):
    __tablename__ = 'Tubular'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    tubulartype_id = Column(String(50), ForeignKey('TubularType.id'), nullable=False)
    outer_diameter = Column(Float, nullable=True)
    inner_diameter = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    yield_strength = Column(Float, nullable=True)
    capacity = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    thread = Column(NCHAR(15), nullable=True)
    burst = Column(Float, nullable=True)
    collapse = Column(Float, nullable=True)
    drift = Column(Float, nullable=True)
    oh_diameter = Column(Float, nullable=True)
    liner_Overlap = Column(Float, nullable=True)
    start_depth = Column(Float, nullable=True)
    end_depth = Column(Float, nullable=True)
    liner_top_depth = Column(NCHAR(10), nullable=True)

    # Relationships
    tubular_type = relationship('TubularType', back_populates='tubulars')

#tubularType
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class TubularType(Base):
    __tablename__ = 'TubularType'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    type = Column(String(15), nullable=True)
    type_short = Column(String(3), nullable=True)
    description = Column(String(50), nullable=True)

    # Relationships
    tubulars = relationship('Tubular', back_populates='tubular_type')


#user
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def utcnow():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = 'user'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    full_name = Column(String(50), nullable=True)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=True)
    is_verified = Column(Boolean, nullable=True)
    verification_token = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=utcnow, nullable=True)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=True)

    # Relationships
    password_resets = relationship('PasswordReset', back_populates='user')
    user_sessions = relationship('UserSession', back_populates='user')

    def __repr__(self):
        return f"<User {self.id}>"

#user_session
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def utcnow():
    return datetime.now(timezone.utc)

class UserSession(Base):
    __tablename__ = 'user_session'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    user_id = Column(String(50), ForeignKey('user.id'), nullable=False)
    access_token = Column(String(50), nullable=False)
    refresh_token = Column(String(50), nullable=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=True)
    last_activity = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=True)
    device_info = Column(String(50), nullable=True)
    ip_address = Column(String(50), nullable=True)

    # Relationships
    user = relationship('User', back_populates='user_sessions')

#well_control_Equipment
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class WellControlEquipment(Base):
    __tablename__ = 'well_control_Equipment'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    rig_id = Column(String(50), ForeignKey('rig.id'), nullable=False)
    choke_line_diameter = Column(Float, nullable=True)
    choke_line_pressure = Column(Float, nullable=True)
    kill_line_diameter = Column(Float, nullable=True)
    bop_size = Column(Float, nullable=True)
    bop_max_pressure = Column(Float, nullable=True)
    bop_max_temperature = Column(Float, nullable=True)
    diverter_manufacturer = Column(String(25), nullable=True)
    diverter_model = Column(String(25), nullable=True)
    line_number = Column(Integer, nullable=True)
    internal_diameter = Column(Float, nullable=True)
    max_pressure = Column(Float, nullable=True)
    line_length = Column(Float, nullable=True)
    closing_time = Column(Float, nullable=True)

    # Relationships
    rig = relationship('Rig', back_populates='well_control_equipments')

#wellbore
from sqlalchemy import Column, String, Float, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Wellbore(Base):
    __tablename__ = 'Wellbore'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    job_id = Column(String(50), ForeignKey('job.id'), nullable=False)
    short_name = Column(String(10), nullable=False)
    wellbore_name = Column(String(25), nullable=False)
    wellbore_number = Column(String(25), nullable=True)
    contract_type_id = Column(Integer, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    primary_currency = Column(String(10), nullable=True)
    secondary_currency = Column(String(10), nullable=True)
    planned_start_date = Column(Date, nullable=True)
    Planned_days = Column(Integer, nullable=True)
    Planned_well_cost = Column(Float, nullable=True)
    actual_well_cost = Column(Float, nullable=True)

    # Relationships
    job = relationship('Job', back_populates='wellbores')
    tallies = relationship('Tally', back_populates='wellbore')
    time_sheets = relationship('TimeSheet', back_populates='wellbore')
    mud_equipment_details = relationship('MudEquipmentDetail', back_populates='wellbore')
    mud_pump_details = relationship('MudPumpDetail', back_populates='wellbore')
    physical_barriers = relationship('PhysicalBarrier', back_populates='wellbore')
    operational_parameters = relationship('OperationalParameters', back_populates='wellbore')
    trajectories = relationship('Trajectory', back_populates='wellbore')

#wellbore_geometry
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class WellboreGeometry(Base):
    __tablename__ = 'wellbore_geometry'

    id = Column(String(50), primary_key=True, default=generate_uuid)
    wellbore_id = Column(String(50),
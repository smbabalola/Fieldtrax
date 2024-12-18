#operational_parameters
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class OperationalParameterBase(TimeStampSchema):
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
    
class OperationalParameterCreate(OperationalParameterBase):
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
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class OperationalParameterUpdate(OperationalParameterBase):
    pass

class OperationalParameterResponse(OperationalParameterBase):
    id: str

    class Config:
        from_attributes = True

class OperationalParameterView(OperationalParameterResponse):
    pass
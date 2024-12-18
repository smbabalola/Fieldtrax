#job_parameter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class JobParameterBase(TimeStampSchema):
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

class JobParameterCreate(JobParameterBase):
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
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
        
class JobParameterUpdate(JobParameterBase):
    pass

class JobParameterResponse(JobParameterBase):
    id: str

    class Config:
        from_attributes = True

class JobParameterView(JobParameterBase):
    pass
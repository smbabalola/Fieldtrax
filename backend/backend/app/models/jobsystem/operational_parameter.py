from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean, Text

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class OperationalParameter(BaseDBModel):
    __tablename__ = 'operational_parameters'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=True)
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

    wellbore = relationship('Wellbore', back_populates='operational_parameters') 

    def __repr__(self):
        return f"<OperationalParameter: {self.zone}>"
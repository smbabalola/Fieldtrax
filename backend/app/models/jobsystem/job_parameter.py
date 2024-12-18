from sqlalchemy import Column, String, Integer, ForeignKey, Float

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class JobParameter(BaseDBModel):
    __tablename__ = 'job_parameters'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=True)
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

    wellbore = relationship('Wellbore', back_populates='job_parameters') 

    def __repr__(self):
        return f"<JobParameter: {self.wellbore_id}>"
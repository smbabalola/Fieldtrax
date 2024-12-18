from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class RigEquipment(BaseDBModel):
    __tablename__ = 'rig_equipments'

    rig_id = Column(String(50), ForeignKey('rigs.id'), nullable=False)
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

    rig = relationship('Rig', back_populates='rig_equipments') 

    def __repr__(self):
        return f"<RigEquipment: {self.rig_id}>"

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class WellControlEquipment(BaseDBModel):
    __tablename__ = 'well_control_equipments'

    rig_id = Column(String(50), ForeignKey('rigs.id'), nullable=False)
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

    rig = relationship('Rig', back_populates='well_control_equipments') 

    def __repr__(self):
        return f"<WellControlEquipment: {self.rig_id}>"

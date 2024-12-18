from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class MudPump(BaseDBModel):
    __tablename__ = 'mud_pumps'

    rig_id = Column(String(50), ForeignKey('rigs.id'), nullable=False)
    serial_number = Column(String(25), nullable=True)
    stroke_length = Column(Float, nullable=True)
    max_pressure = Column(Float, nullable=True)
    power_rating = Column(Float, nullable=True)
    manufacturer = Column(String(25), nullable=True)
    model = Column(String(25), nullable=True)
    efficiency = Column(Float, nullable=True)
    pump_type = Column(String(25), nullable=True)

    rig = relationship('Rig', back_populates='mud_pumps') 
    mud_pump_details = relationship('MudPumpDetail', back_populates='mud_pump')

    def __repr__(self):
        return f"<MudPump: {self.serial_number or ''}>"



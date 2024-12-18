from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class RotaryEquipment(BaseDBModel):
    __tablename__ = 'rotary_equipments'

    rig_id = Column(String(50), ForeignKey('rigs.id'), nullable=False)
    top_drive_manufacturer = Column(String(25), nullable=True)
    top_drive_model = Column(String(25), nullable=True)
    top_drive_power_rating = Column(Float, nullable=True)
    top_drive_torque_rating = Column(Float, nullable=True)
    top_drive_weight = Column(Float, nullable=True)
    rotary_table_manufacturer = Column(String(25), nullable=True)
    rotary_table_model = Column(String(25), nullable=True)
    rotary_table_power_rating = Column(Float, nullable=True)
    rotary_table_torque_rating = Column(Float, nullable=True)

    rig = relationship('Rig', back_populates='rotary_equipments') 

    def __repr__(self):
        return f"<RotaryEquipment: {self.rig_id}>"
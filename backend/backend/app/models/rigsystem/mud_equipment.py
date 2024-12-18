from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class MudEquipment(BaseDBModel):
    __tablename__ = 'mud_equipments'

    rig_id = Column(String(50), ForeignKey('rigs.id'), nullable=False)
    equipment_name = Column(String(25), nullable=True)
    serial_number = Column(String(25), nullable=True)
    manufacturer = Column(String(25), nullable=True)
    model = Column(String(25), nullable=True)

    rig = relationship('Rig', back_populates='mud_equipments') 
    mud_equipment_details = relationship('MudEquipmentDetail', back_populates='mud_equipment')  
    def __repr__(self):
        return f"<MudEquipment: {self.equipment_name}>"
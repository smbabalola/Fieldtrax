from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.base import BaseDBModel

class Rig(BaseDBModel):
    __tablename__ = 'rigs'

    rig_name = Column(String(25), nullable=False)
    contractor_id = Column(String(50), ForeignKey('contractors.id'), nullable=False)
    rig_type_id = Column(String(50), ForeignKey('rig_types.id'), nullable=False)
    air_gap = Column(Float, nullable=True)
    water_depth = Column(Float, nullable=True)

    # Relationships
    contractor = relationship('Contractor', back_populates='rigs') #confirmed!
    mud_equipments = relationship('MudEquipment', back_populates='rig') #confirmed
    mud_pumps = relationship('MudPump', back_populates='rig') #confirmed!
    well_control_equipments = relationship('WellControlEquipment', back_populates='rig') #confirmed!
    rig_equipments = relationship('RigEquipment', back_populates='rig') #confirmed!
    rig_stabilitys = relationship('RigStability', back_populates='rig') #confirmed!
    rotary_equipments = relationship('RotaryEquipment', back_populates='rig') #confirmed
    tanks = relationship('Tank', back_populates='rig') #confirmed!
    jobs = relationship('Job', back_populates='rig') #confirmed!
    rig_type = relationship('RigType', back_populates='rigs') #confirmed!

    def __repr__(self):
        return f"<Rig: {self.rig_name}>"




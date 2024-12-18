from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class RigStability(BaseDBModel):
    __tablename__ = 'rig_stabilitys'

    rig_id = Column(String(50), ForeignKey('rigs.id'), nullable=False)
    max_deck_load_op_draft = Column(Float, nullable=True)
    max_deck_load_survival_draft = Column(Float, nullable=True)
    max_deck_load_transit_draft = Column(Float, nullable=True)
    max_deck_load_water_depth = Column(Float, nullable=True)
    number_thrusters = Column(Integer, nullable=True)
    thruster_power = Column(Float, nullable=True)
    number_anchors = Column(Integer, nullable=True)
    number_riser_tensioners = Column(Integer, nullable=True)
    number_guideline_tensioners = Column(Integer, nullable=True)

    rig = relationship('Rig', back_populates='rig_stabilitys') 

    def __repr__(self):
        return f"<RigStability: {self.rig_id}>"
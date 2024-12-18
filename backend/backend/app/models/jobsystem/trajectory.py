from sqlalchemy import Column, String, Integer, ForeignKey, Float

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class Trajectory(BaseDBModel):
    __tablename__ = 'trajectorys'
    __table_args__ = {'extend_existing': True} 

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=False)
    measured_depth = Column(Float, nullable=False)
    inclination = Column(Float, nullable=False)
    azimuth = Column(Float, nullable=False)

    wellbore = relationship('Wellbore', back_populates='trajectories') 

    def __repr__(self):
        return f"<Trajectory: {self.wellbore_id}>"
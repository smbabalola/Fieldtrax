from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class PhysicalBarrier(BaseDBModel):
    __tablename__ = 'physical_barriers'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=False)
    barrier_type = Column(String(50), nullable=False)
    depth_value = Column(Float, nullable=False)
    depth_unit = Column(String(50), nullable=True)
    length_value = Column(Float, nullable=True)
    length_unit = Column(String(50), nullable=True)
    pressure_rating_value = Column(Float, nullable=False)
    pressure_rating_unit = Column(String(50), nullable=True)
    installation_date = Column(DateTime, nullable=False)
    installed_by = Column(String(50), nullable=False)
    verified_by = Column(String(50), nullable=True)
    verification_date = Column(DateTime, nullable=True)

    wellbore = relationship('Wellbore', back_populates='physical_barriers') 

    def __repr__(self):
        return f"<PhysicalBarrier: {self.barrier_type}>"
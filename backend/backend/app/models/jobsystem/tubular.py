from sqlalchemy import Column, String, Integer, ForeignKey, Float, NCHAR

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel
from app.models.jobsystem.wellbore_geometry import WellboreGeometry

class Tubular(BaseDBModel):
    __tablename__ = 'tubulars'

    tubulartype_id = Column(Integer, ForeignKey('tubular_types.id'), nullable=False)
    outer_diameter = Column(Float, nullable=True)
    inner_diameter = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    yield_strength = Column(Float, nullable=True)
    capacity = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    thread = Column(NCHAR(15), nullable=True)
    burst = Column(Float, nullable=True)
    collapse = Column(Float, nullable=True)
    drift = Column(Float, nullable=True)
    oh_diameter = Column(Float, nullable=True)
    liner_Overlap = Column(Float, nullable=True)
    start_depth = Column(Float, nullable=True)
    end_depth = Column(Float, nullable=True)
    liner_top_depth = Column(NCHAR(10), nullable=True)

    tubular_type = relationship('TubularType', back_populates='tubulars')
    wellbore_geometries = relationship('WellboreGeometry', back_populates='tubular') 

    def __repr__(self):
        return f"<Tubular: {self.tubulartype_id}>"
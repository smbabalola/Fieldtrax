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
    grade = Column(String(15), nullable=True)
    thread = Column(String(15), nullable=True)
    open_hole_size = Column(Float, nullable=True)
    yield_strength = Column(Float, nullable=True)
    capacity = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    thread = Column(NCHAR(15), nullable=True)
    burst = Column(Float, nullable=True)
    collapse = Column(Float, nullable=True)
    drift = Column(Float, nullable=True)
    oh_diameter = Column(Float, nullable=True)
    start_depth = Column(Float, nullable=True)
    end_depth = Column(Float, nullable=True)
    remarks = Column(String(50), nullable=True)
    
    tubular_type = relationship('TubularType', back_populates='tubulars')
    wellbore_geometries = relationship('WellboreGeometry', back_populates='tubular') 
    
    __mapper_args__ = {
        'polymorphic_identity': 'tubular', # important
        'polymorphic_on': tubulartype_id  # important
    }
    
    
class Casing(Tubular):
    __tablename__ = 'casings' # Separate table for casings

    id = Column(Integer, ForeignKey('tubulars.id'), primary_key=True)
    cement_top = Column(Float, nullable=True)
    cement_yield = Column(Float, nullable=True)
    

    __mapper_args__ = {
        'polymorphic_identity': 'casing', # important
    }

class Liner(Tubular):
    __tablename__ = 'liners' # Separate table for liners

    id = Column(Integer, ForeignKey('tubulars.id'), primary_key=True)
    liner_top = Column(Float, nullable=True)
    liner_bottom = Column(Float, nullable=True)
    bht_at_liner_top = Column(Float, nullable=True)
    liner_top_depth = Column(Float, nullable=True)
    liner_top_deviation = Column(Float, nullable=True)
    liner_shoe_deviation = Column(Float, nullable=True)
    liner_Overlap_length = Column(Float, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'liner', # important
    }

class Drillstring(Tubular):
    __tablename__ = 'drillstrings' # Separate table for drillstrings

    id = Column(Integer, ForeignKey('tubulars.id'), primary_key=True)
    component_type = Column(String(50), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'drillstring', # important
    }

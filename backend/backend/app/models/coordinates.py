from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class ReferenceLocation(BaseModel):
    __tablename__ = 'reference_locations'

    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
    coordinate_system = Column(String(50))
    utm_zone = Column(String(10))
    description = Column(String(200))

class Coordinates(BaseModel):
    __tablename__ = 'coordinates'

    reference_id = Column(String(36), ForeignKey('reference_locations.id'))
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    
    # Relationships
    reference = relationship("ReferenceLocation")
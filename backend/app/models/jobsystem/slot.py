from sqlalchemy import Column, String, Integer, ForeignKey, Float

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class Slot(BaseDBModel):
    __tablename__ = 'slots'

    installation_id = Column(String(50), ForeignKey("installations.id"), nullable=True)
    slot_name = Column(String(50), nullable=True)
    utm_eastings = Column(Float, nullable=True)
    utm_northings = Column(Float, nullable=True)
    longitude = Column(String(50), nullable=True)
    latitude = Column(String(50), nullable=True)

    installation = relationship('Installation', back_populates='slots')
    wells = relationship('Well', back_populates='slot') 

    def __repr__(self):
        return f"<Slot: {self.slot_name}>"
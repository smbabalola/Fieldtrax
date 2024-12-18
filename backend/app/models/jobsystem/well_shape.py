from sqlalchemy import Column, String

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class WellShape(BaseDBModel):
    __tablename__ = 'well_shapes'

    well_shape = Column(String(25), nullable=False)
    description = Column(String(50), nullable=False)

    wells = relationship('Well', back_populates='well_shape') 

    def __repr__(self):
        return f"<WellShape: {self.well_shape}>"
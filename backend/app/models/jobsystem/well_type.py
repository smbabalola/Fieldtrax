from sqlalchemy import Column, String

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class WellType(BaseDBModel):
    __tablename__ = 'well_types'

    well_type_name = Column(String(25), nullable=False)
    description = Column(String(255), nullable=False)

    wells = relationship('Well', back_populates='well_type') 

    def __repr__(self):
        return f"<WellType: {self.well_type_name}>"
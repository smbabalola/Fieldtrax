from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class Backload(BaseDBModel):
    __tablename__ = 'backloads'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=False)
    sheet_number = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)
    destination = Column(String(50), nullable=False)
    total_weight_value = Column(Float, nullable=False)
    total_weight_unit = Column(String(50), nullable=True)
    transportation_details = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)
    approved_by = Column(String(50), nullable=True)

    wellbore = relationship('Wellbore', back_populates='backloads') 

    def __repr__(self):
        return f"<Backload: {self.sheet_number}>"
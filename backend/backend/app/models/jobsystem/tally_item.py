from sqlalchemy import Column, String, Integer, ForeignKey, Float, Text

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class TallyItem(BaseDBModel):
    __tablename__ = 'tally_items'

    tally_id = Column(String(50), ForeignKey('tallys.id'), nullable=False)
    length_value = Column(Float, nullable=False)
    length_unit = Column(String(50), nullable=True)
    outer_diameter_value = Column(Float, nullable=False)
    outer_diameter_unit = Column(String(50), nullable=True)
    inner_diameter_value = Column(Float, nullable=True)
    inner_diameter_unit = Column(String(50), nullable=True)
    weight_per_unit_value = Column(Float, nullable=False)
    weight_per_unit_unit = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    serial_number = Column(String(50), nullable=True)

    tally = relationship('Tally', back_populates='tally_items') 

    def __repr__(self):
        return f"<TallyItem: {self.serial_number or ''}>"
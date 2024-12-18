from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class Tally(BaseDBModel):
    __tablename__ = 'tallys'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=False)
    tally_type = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)
    total_length_value = Column(Float, nullable=False)
    total_length_unit = Column(String(50), nullable=True)
    total_weight_value = Column(Float, nullable=False)
    total_weight_unit = Column(String(50), nullable=True)
    verified_by = Column(String(50), nullable=True)

    wellbore = relationship('Wellbore', back_populates='tallys')
    tally_items = relationship('TallyItem', back_populates='tally') 

    def __repr__(self):
        return f"<Tally: {self.tally_type}>"
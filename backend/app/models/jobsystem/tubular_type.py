from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class TubularType(BaseDBModel):
    __tablename__ = 'tubular_types' 

    id = Column(Integer, primary_key=True)
    tubular_type = Column(String(15), nullable=True)
    type_short = Column(String(3), nullable=True)
    description = Column(String(50), nullable=True)

    tubulars = relationship('Tubular', back_populates='tubular_type')



    def __repr__(self):
        return f"<TubularType: {self.tubular_type}>"
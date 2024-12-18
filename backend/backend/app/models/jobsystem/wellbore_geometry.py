from sqlalchemy import Column, String, Integer, ForeignKey

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class WellboreGeometry(BaseDBModel):
    __tablename__ = 'wellbore_geometrys'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=False)
    tubular_id = Column(String(50), ForeignKey('tubulars.id'), nullable=False)

    wellbore = relationship('Wellbore', back_populates='wellbore_geometries')
    tubular = relationship('Tubular', back_populates='wellbore_geometries') 

    def __repr__(self):
        return f"<WellboreGeometry: {self.wellbore_id}>"
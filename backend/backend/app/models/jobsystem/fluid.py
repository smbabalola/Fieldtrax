from sqlalchemy import Column, String, Integer, ForeignKey, Float, Text

from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class Fluid(BaseDBModel):
    __tablename__ = 'fluids'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=False)
    fluid_type = Column(String(50), nullable=False)
    volume_value = Column(Float, nullable=False)
    volume_unit = Column(String(30), nullable=True)
    density_value = Column(Float, nullable=False)
    density_unit = Column(String(30), nullable=True)
    viscosity_value = Column(Float, nullable=True)
    viscosity_unit = Column(String(30), nullable=True)
    description = Column(Text, nullable=True)

    wellbore = relationship('Wellbore', back_populates='fluids') 

    def __repr__(self):
        return f"<Fluid: {self.fluid_type}>"
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Float, Text

from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class Fluid(BaseDBModel):
    __tablename__ = 'fluids'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=False)
    report_date = Column(DateTime, nullable=False)
    sample_from = Column(String(10), nullable=False)
    fluid_type = Column(String(25), nullable=False)
    mud_weight = Column(Float, nullable=False)
    funnel_viscosity = Column(Float, nullable=False)
    plastic_viscosity = Column(Float, nullable=False)
    yield_point = Column(Float, nullable=False)
    gel_strength_10s = Column(Float, nullable=False)
    gel_strength_10m = Column(Float, nullable=False)
    pH = Column(Float, nullable=False)
    r600 = Column(Float, nullable=False)
    r300 = Column(Float, nullable=False)
    r200 = Column(Float, nullable=False)
    r100 = Column(Float, nullable=False)
    r6 = Column(Float, nullable=False)
    r3 = Column(Float, nullable=False)
    test_number = Column(Integer, nullable=False)

    wellbore = relationship('Wellbore', back_populates='fluids') 

    def __repr__(self):
        return f"<Fluid: {self.fluid_type}>"
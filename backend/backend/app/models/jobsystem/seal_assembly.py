from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class SealAssembly(BaseDBModel):
    __tablename__ = 'seal_assemblys'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=True)
    seal_surface_od = Column(Float, nullable=True)
    body_burst = Column(Float, nullable=True)
    collapse = Column(Float, nullable=True)
    tensile = Column(Float, nullable=True)
    tieback_extension_id = Column(Float, nullable=True)
    tieback_extension_burst = Column(Float, nullable=True)
    tieback_extension_collapse = Column(Float, nullable=True)
    tieback_yield_collapse = Column(Float, nullable=True)
    setting_force = Column(Float, nullable=True)
    hold_down_slips = Column(Boolean, nullable=True)
    element_rating = Column(Float, nullable=True)
    slick_stinger_od = Column(Float, nullable=True)

    wellbore = relationship('Wellbore', back_populates='seal_assemblys') 

    def __repr__(self):
        return f"<SealAssembly: {self.wellbore_id}>"
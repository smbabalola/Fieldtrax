from sqlalchemy import Column, String, Integer, ForeignKey, Float

from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class HangerInfo(BaseDBModel):
    __tablename__ = 'hanger_infos'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=True)
    type = Column(String(20), nullable=True)
    burst_rating = Column(Float, nullable=True)
    tensile_rating = Column(Float, nullable=True)
    hanging_capacity = Column(Float, nullable=True)
    hydraulic_setting_pressure = Column(Float, nullable=True)

    wellbore = relationship('Wellbore', back_populates='hanger_infos')

    def __repr__(self):
        return f"<HangerInfo: {self.type}>"
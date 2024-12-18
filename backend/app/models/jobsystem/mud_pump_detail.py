from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class MudPumpDetail(BaseDBModel):
    __tablename__ = 'mud_pump_details'

    report_id = Column(String(50), ForeignKey('daily_reports.id'), nullable=False)
    mud_pump_id = Column(String(50), ForeignKey('mud_pumps.id'), nullable=False)
    circulation_rate = Column(Float, nullable=False)
    for_hole = Column(Boolean, nullable=False)

    daily_report = relationship('DailyReport', back_populates='mud_pump_details')
    mud_pump = relationship('MudPump', back_populates='mud_pump_details') 

    def __repr__(self):
        return f"<MudPumpDetail: {self.mud_pump_id}>"

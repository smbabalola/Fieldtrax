from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class DailyReport(BaseDBModel):
    __tablename__ = 'daily_reports'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=False)
    report_date = Column(DateTime, nullable=False)

    wellbore = relationship('Wellbore', back_populates='daily_reports')
    mud_equipment_details = relationship('MudEquipmentDetail', back_populates='daily_report')
    mud_pump_details = relationship("MudPumpDetail", back_populates='daily_report')

    def __repr__(self):
        return f"<DailyReport: {self.report_date}>"
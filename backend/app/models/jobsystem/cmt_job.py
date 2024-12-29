from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class CMTJOB(BaseDBModel):
    __tablename__ = 'cmt_jobs'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=False)
    off_bottom_cement_type = Column(String, nullable=True)
    open_hole_packer_depth = Column(float, nullable=True)
    open_hole_packers = Column(Boolean, nullable=True)
    screen_supplier = Column(String(50), nullable=True)
    fluid_loss = Column(Boolean, nullable=True)
    pac_valve_depth = Column(float, nullable=True) 
    packer_above_screens = Column(Boolean, nullable=True)
    pressure_below_ECP = Column(float, nullable=True)
    
    wellbore = relationship('Wellbore', back_populates='daily_reports')
    mud_equipment_details = relationship('MudEquipmentDetail', back_populates='daily_report')
    mud_pump_details = relationship("MudPumpDetail", back_populates='daily_report')

    def __repr__(self):
        return f"<DailyReport: {self.report_date}>"
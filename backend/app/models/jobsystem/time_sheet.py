from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, Boolean, Text

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class TimeSheet(BaseDBModel):
    __tablename__ = 'time_sheets'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=False)
    job_id = Column(String(50), ForeignKey('jobs.id'), nullable=False)
    employee_id = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)
    hours_worked = Column(Float, nullable=False)
    activity_code = Column(String(1), nullable=False)
    description = Column(Text, nullable=True)
    approved = Column(Boolean, nullable=True)
    approved_by = Column(String(50), nullable=True)
    approval_date = Column(DateTime, nullable=True)

    wellbore = relationship('Wellbore', back_populates='time_sheets')
    job = relationship('Job', back_populates='time_sheets') 

    def __repr__(self):
        return f"<TimeSheet: {self.employee_id}>"
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class JobLog(BaseDBModel):
    __tablename__ = 'job_logs'

    job_id = Column(String(50), ForeignKey('jobs.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    activity_type = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    duration = Column(Float, nullable=True)

    job = relationship('Job', back_populates='job_logs') 

    def __repr__(self):
        return f"<JobLog: {self.activity_type}>"
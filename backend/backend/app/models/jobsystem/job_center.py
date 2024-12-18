from sqlalchemy import Column, String, Integer, ForeignKey

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class JobCenter(BaseDBModel):
    __tablename__ = 'job_centers'

    # Job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    job_center_name = Column(String(100), nullable=True)
    description = Column(String(255), nullable=True)

    jobs = relationship('Job', back_populates='job_center') 

    def __repr__(self):
        return f"<JobCenter: {self.short_name}>"
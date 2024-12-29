from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, UUID
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class Activity(BaseDBModel):
    __tablename__ = "activities"

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(String(50), ForeignKey("jobs.id"), nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    type = Column(Enum("mobilization", "demobilization", "equipment_delivery", "start_job", "end_job", "incident","NPT", name="activity_type"), nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)

    job = relationship("Job", back_populates="activities")
    user = relationship("User", back_populates="activities")

    def __repr__(self):
        return f"<Activity(id={self.id}, job_id={self.job_id}, type={self.type}, timestamp={self.timestamp})>"
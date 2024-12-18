from sqlalchemy import NCHAR, Column, String, Integer, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.base import BaseDBModel

class Job(BaseDBModel):
    __tablename__ = 'jobs'

    jobcenter_id = Column(String(50), ForeignKey('job_centers.id'), nullable=False)
    job_name = Column(String(50), nullable=False)
    job_description = Column(String(100), nullable=True)
    rig_id = Column(String(50), ForeignKey('rigs.id'), nullable=False)
    purchase_order_id = Column(String(50), ForeignKey('purchase_orders.id'), nullable=False)
    operator_id = Column(String(50), ForeignKey('operators.id'), nullable=False)
    well_id = Column(String(50), ForeignKey('wells.id'), nullable=False)
    service_code = Column(NCHAR(4), nullable=True)
    country = Column(String(50), nullable=False)
    measured_depth = Column(Float, nullable=True)
    total_vertical_depth = Column(String(10), nullable=True)
    spud_date = Column(DateTime, nullable=False)
    status = Column(String(30), nullable=True)
    mobilization_date = Column(DateTime, nullable=True)
    demobilization_date = Column(DateTime, nullable=True)
    job_closed = Column(Boolean, nullable=True)
    trainingfile = Column(Boolean, nullable=True)

    # Relationships
    job_center = relationship('JobCenter', back_populates='jobs')
    well = relationship('Well', back_populates='jobs') 
    job_logs =  relationship('JobLog', back_populates='job') 
    time_sheets = relationship('TimeSheet', back_populates='job') 
    rig = relationship('Rig', back_populates='jobs') 
    operator = relationship('Operator', back_populates='jobs') 
    purchase_order = relationship('PurchaseOrder', back_populates='jobs') 

    def __repr__(self):
        return f"<Job: {self.well_name}>"


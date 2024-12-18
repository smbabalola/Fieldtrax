from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime, Float, Text

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class Wellbore(BaseDBModel):
    __tablename__ = 'wellbores'

    well_id = Column(String(50), ForeignKey('wells.id'), nullable=False)
    short_name = Column(String(10), nullable=False)
    wellbore_name = Column(String(25), nullable=False)
    description = Column(Text, nullable=True)
    wellbore_number = Column(String(25), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    primary_currency = Column(String(10), nullable=True)
    secondary_currency = Column(String(10), nullable=True)
    planned_start_date = Column(Date, nullable=True)
    Planned_days = Column(Integer, nullable=True)
    Planned_well_cost = Column(Float, nullable=True)
    actual_well_cost = Column(Float, nullable=True)

    backloads = relationship('Backload', back_populates='wellbore')
    daily_reports = relationship('DailyReport', back_populates='wellbore')
    fluids = relationship('Fluid', back_populates='wellbore')
    hanger_infos = relationship('HangerInfo', back_populates='wellbore')
    job_parameters = relationship('JobParameter', back_populates='wellbore')
    seal_assemblys = relationship('SealAssembly', back_populates='wellbore')
    tallys = relationship('Tally', back_populates='wellbore')
    time_sheets = relationship('TimeSheet', back_populates='wellbore')
    physical_barriers = relationship('PhysicalBarrier', back_populates='wellbore')
    operational_parameters = relationship('OperationalParameter', back_populates='wellbore')
    trajectories = relationship('Trajectory', back_populates='wellbore')
    wellbore_geometries = relationship('WellboreGeometry', back_populates='wellbore')
    delivery_tickets = relationship('DeliveryTicket', back_populates='wellbore')
    # purchase_orders = relationship('PurchaseOrder', back_populates='wellbore')
    well = relationship('Well', back_populates='wellbores') 

    def __repr__(self):
        return f"<Wellbore: {self.wellbore_name}>"
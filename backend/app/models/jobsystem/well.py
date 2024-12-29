from sqlalchemy import Boolean, Column, Numeric, String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class Well(BaseDBModel):
    __tablename__ = 'wells'
    
    slot_id = Column(String(50), ForeignKey("slots.id"), nullable=False)
    well_name = Column(String(100), nullable=False)
    short_name = Column(String(50))
    formation_type = Column(String(100), nullable=True)
    api_number = Column(String(20))
    spud_date = Column(DateTime(timezone=True))
    well_type_id = Column(String(50), ForeignKey("well_types.id"))
    production_id = Column(String(50), ForeignKey("productions.id"))
    well_shape_id = Column(String(50), ForeignKey("well_shapes.id"))
    operator_id = Column(String(50), ForeignKey("operators.id"))
    measured_depth = Column(Float, default=0)
    total_vertical_depth = Column(Float, default=0)
    h2s = Column(Boolean, nullable=True)
    co2 = Column(Boolean, nullable=True)

    slot = relationship('Slot', back_populates='wells')
    jobs = relationship('Job', back_populates='well')
    well_type = relationship('WellType', back_populates='wells')
    production = relationship('Production', back_populates='wells')
    well_shape = relationship('WellShape', back_populates='wells')
    wellbores = relationship('Wellbore', back_populates='well')
    # field = relationship('Field', back_populates='wells')
    purchase_orders = relationship('PurchaseOrder', back_populates='well') 
    operator = relationship('Operator', back_populates='wells')

    def __repr__(self):
        return f"<Well: {self.well_name}>"
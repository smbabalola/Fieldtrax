from sqlalchemy import Column, String, Integer, ForeignKey, Float, NCHAR

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class PurchaseOrderItem(BaseDBModel):
    __tablename__ = 'purchase_order_items'

    purchase_order_id = Column(String(50), ForeignKey('purchase_orders.id'), nullable=True)
    item_no = Column(String(50), nullable=True)
    service_code = Column(NCHAR(10), nullable=True)
    sp_code = Column(NCHAR(10), nullable=True) 
    description = Column(String(50), nullable=True)
    quantity = Column(Integer, nullable=True)
    unit_of_measure = Column(NCHAR(10), nullable=True)
    unit_price = Column(String(50), nullable=True)
    extended_price = Column(Float, nullable=True)
    tax = Column(Float, nullable=True)
    discounts = Column(Float, nullable=True)

    purchase_order = relationship('PurchaseOrder', back_populates='purchase_order_items') 

    def __repr__(self):
        return f"<PurchaseOrderItem: {self.item_no}>"

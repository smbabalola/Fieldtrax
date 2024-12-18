# File: app/models/jobsystem/purchase_order.py
from sqlalchemy import Column, ForeignKey, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base, BaseDBModel
import uuid
from sqlalchemy.orm import relationship

class PurchaseOrder(BaseDBModel):
    __tablename__ = "purchase_orders"

    well_id = Column(String(50),  ForeignKey('wells.id'), nullable=False)
    po_number = Column(String(50), nullable=False)
    contract_no = Column(String(50))
    vendor_no = Column(String(50))
    DRSS_no = Column(String(50))
    po_date = Column(DateTime(timezone=True), nullable=False)  # Changed to DateTime
    supplier_name = Column(String(100))
    supplier_address1 = Column(String(100))
    supplier_address2 = Column(String(100))
    county = Column(String(50))
    country = Column(String(50))
    supplier_contact = Column(String(100))
    supplier_contact_information = Column(String(100))
    buyer_name = Column(String(100))
    buyer_address1 = Column(String(100))
    buyer_address_2 = Column(String(100))
    buyer_contact_information = Column(String(100))
    delievry_address1 = Column(String(100))
    delivery_address2 = Column(String(100))
    delievry_postcode = Column(String(20))
    delivery_zipcode = Column(String(20))
    payment_terms = Column(String(100))
    shipping_terms = Column(String(100))

    well = relationship('Well', back_populates='purchase_orders')
    purchase_order_items = relationship('PurchaseOrderItem', back_populates='purchase_order')
    delivery_tickets = relationship('DeliveryTicket', back_populates='purchase_order') 
    jobs = relationship('Job', back_populates='purchase_order')

    def __repr__(self):
        return f"<PurchaseOrder: {self.po_number}>"
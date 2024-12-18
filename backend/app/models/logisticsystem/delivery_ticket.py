from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class DeliveryTicket(BaseDBModel):
    __tablename__ = 'delivery_tickets'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=False)
    purchase_order_id = Column(String(50), ForeignKey('purchase_orders.id'), nullable=False)
    shipped_via = Column(String(50), nullable=True)
    ticket_number = Column(String(50), nullable=False)
    delivery_date = Column(DateTime, nullable=False)
    supplier = Column(String(50), nullable=False)
    total_amount = Column(Float, nullable=False)
    currency = Column(String(50), nullable=True)
    received_by = Column(String(50), nullable=False)
    status = Column(String(50), nullable=True)

    wellbore = relationship('Wellbore', back_populates='delivery_tickets')
    purchase_order = relationship('PurchaseOrder', back_populates='delivery_tickets')
    delivery_ticket_items = relationship('DeliveryTicketItem', back_populates='delivery_ticket') 

    def __repr__(self):
        return f"<DeliveryTicket: {self.ticket_number}>"

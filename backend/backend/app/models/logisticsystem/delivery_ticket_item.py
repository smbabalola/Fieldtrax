from sqlalchemy import Column, String, Integer, ForeignKey

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class DeliveryTicketItem(BaseDBModel):
    __tablename__ = 'delivery_ticket_items'

    delivery_ticket_id = Column(String(50), ForeignKey('delivery_tickets.id'), nullable=False)
    material_type = Column(String(50), nullable=False)
    item_no = Column(Integer, nullable=False)
    stock_no = Column(Integer, nullable=False)
    description = Column(String(50), nullable=False)
    kit_no = Column(String(20), nullable=True)

    delivery_ticket = relationship('DeliveryTicket', back_populates='delivery_ticket_items')

    def __repr__(self):
        return f"<DeliveryTicketItem: {self.item_no}>"
    
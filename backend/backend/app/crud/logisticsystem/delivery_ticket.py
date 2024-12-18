# File: backend/app/crud/logisticssystem/crud_delivery_ticket.py
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.logisticsystem.delivery_ticket import DeliveryTicket
from app.schemas.logisticsystem.delivery_ticket import DeliveryTicketCreate, DeliveryTicketUpdate

class CRUDDeliveryTicket(CRUDBase[DeliveryTicket, DeliveryTicketCreate, DeliveryTicketUpdate]):
    async def get_by_ticket_number(
        self, 
        db: Session, 
        *, 
        ticket_number: str
    ) -> Optional[DeliveryTicket]:
        """Get delivery ticket by number"""
        return db.query(DeliveryTicket).filter(
            DeliveryTicket.ticket_number == ticket_number
        ).first()

    async def get_by_wellbore(
        self,
        db: Session,
        *,
        wellbore_id: str
    ) -> List[DeliveryTicket]:
        """Get all delivery tickets for a wellbore"""
        return db.query(DeliveryTicket).filter(
            DeliveryTicket.wellbore_id == wellbore_id
        ).order_by(DeliveryTicket.delivery_date.desc()).all()

    async def get_by_purchase_order(
        self,
        db: Session,
        *,
        purchase_order_id: str
    ) -> List[DeliveryTicket]:
        """Get all delivery tickets for a purchase order"""
        return db.query(DeliveryTicket).filter(
            DeliveryTicket.purchase_order_id == purchase_order_id
        ).order_by(DeliveryTicket.delivery_date.desc()).all()

    async def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
        wellbore_id: Optional[str] = None
    ) -> List[DeliveryTicket]:
        """Get delivery tickets within a date range"""
        query = db.query(DeliveryTicket).filter(
            DeliveryTicket.delivery_date >= start_date,
            DeliveryTicket.delivery_date <= end_date
        )
        if wellbore_id:
            query = query.filter(DeliveryTicket.wellbore_id == wellbore_id)
        return query.order_by(DeliveryTicket.delivery_date.desc()).all()

crud_delivery_ticket = CRUDDeliveryTicket(DeliveryTicket)


# from app.models.logisticsystem.delivery_ticket import DeliveryTicket
# from app.crud.base import CRUDBase

# crud_delivery_ticket = CRUDBase(DeliveryTicket)
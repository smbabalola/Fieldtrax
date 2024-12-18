# File: backend/app/crud/logisticssystem/crud_delivery_ticket_item.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.logisticsystem.delivery_ticket_item import DeliveryTicketItem
from app.schemas.logisticsystem.delivery_ticket_item import (
    DeliveryTicketItemCreate, 
    DeliveryTicketItemUpdate
)

class CRUDDeliveryTicketItem(CRUDBase[DeliveryTicketItem, DeliveryTicketItemCreate, DeliveryTicketItemUpdate]):
    async def get_by_delivery_ticket(
        self,
        db: Session,
        *,
        delivery_ticket_id: str
    ) -> List[DeliveryTicketItem]:
        """Get all items for a delivery ticket"""
        return db.query(DeliveryTicketItem).filter(
            DeliveryTicketItem.delivery_ticket_id == delivery_ticket_id
        ).order_by(DeliveryTicketItem.item_no).all()

    async def get_by_material_type(
        self,
        db: Session,
        *,
        delivery_ticket_id: str,
        material_type: str
    ) -> List[DeliveryTicketItem]:
        """Get items by material type"""
        return db.query(DeliveryTicketItem).filter(
            DeliveryTicketItem.delivery_ticket_id == delivery_ticket_id,
            DeliveryTicketItem.material_type == material_type
        ).order_by(DeliveryTicketItem.item_no).all()

crud_delivery_ticket_item = CRUDDeliveryTicketItem(DeliveryTicketItem)

# from app.models.logisticsystem.delivery_ticket_item import DeliveryTicketItem
# from app.crud.base import CRUDBase

# crud_delivery_ticket_item = CRUDBase(DeliveryTicketItem)
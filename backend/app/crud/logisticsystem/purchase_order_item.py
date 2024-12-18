# File: backend/app/crud/logisticssystem/crud_purchase_order_item.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.logisticssystem.purchase_order_item import PurchaseOrderItem
from app.schemas.logisticssystem.purchase_order_item import (
    PurchaseOrderItemCreate,
    PurchaseOrderItemUpdate
)

class CRUDPurchaseOrderItem(CRUDBase[PurchaseOrderItem, PurchaseOrderItemCreate, PurchaseOrderItemUpdate]):
    async def get_by_purchase_order(
        self,
        db: Session,
        *,
        purchase_order_id: str
    ) -> List[PurchaseOrderItem]:
        """Get all items for a purchase order"""
        return db.query(PurchaseOrderItem).filter(
            PurchaseOrderItem.purchase_order_id == purchase_order_id
        ).order_by(PurchaseOrderItem.item_no).all()

    async def get_by_service_code(
        self,
        db: Session,
        *,
        service_code: str,
        purchase_order_id: Optional[str] = None
    ) -> List[PurchaseOrderItem]:
        """Get items by service code"""
        query = db.query(PurchaseOrderItem).filter(
            PurchaseOrderItem.service_code == service_code
        )
        if purchase_order_id:
            query = query.filter(PurchaseOrderItem.purchase_order_id == purchase_order_id)
        return query.order_by(PurchaseOrderItem.item_no).all()

    async def calculate_total_amount(
        self,
        db: Session,
        *,
        purchase_order_id: str
    ) -> float:
        """Calculate total amount for a purchase order"""
        items = await self.get_by_purchase_order(db=db, purchase_order_id=purchase_order_id)
        total = sum(
            (item.quantity * float(item.unit_price) if item.unit_price else 0)
            - (item.discounts or 0)
            + (item.tax or 0)
            for item in items
        )
        return total


crud_purchase_order_item = CRUDPurchaseOrderItem(PurchaseOrderItem)

# from app.models.logisticsystem.purchase_order_item import PurchaseOrderItem
# from app.crud.base import CRUDBase

# crud_purchase_order_item = CRUDBase(PurchaseOrderItem)
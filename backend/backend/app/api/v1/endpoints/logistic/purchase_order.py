# File: backend/app/api/v1/endpoints/logisticssystem/purchase_order.py
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.authsystem.user import User
from app.api import deps
from app.crud.logisticsystem.purchase_order import crud_purchase_order
from app.models.logisticsystem.purchase_order import PurchaseOrder
from app.schemas.logisticsystem.purchase_order import (
    PurchaseOrderCreate,
    PurchaseOrderUpdate,
    PurchaseOrderResponse
)

router = APIRouter()
# crud_purchase_order = CRUDPurchaseOrder(PurchaseOrder)

@router.get("/", response_model=List[PurchaseOrderResponse])
async def read_purchase_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve purchase orders.
    """
    purchase_orders = await crud_purchase_order.get_multi(
        db, skip=skip, limit=limit
    )
    return purchase_orders

@router.post("/", response_model=PurchaseOrderResponse)
async def create_purchase_order(
    *,
    db: Session = Depends(deps.get_db),
    purchase_order_in: PurchaseOrderCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create new purchase order.
    """
    purchase_order = await crud_purchase_order.create(
        db=db, obj_in=purchase_order_in
    )
    return purchase_order
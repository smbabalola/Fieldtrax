#purchaseOrderItems
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class PurchaseOrderItemBase(TimeStampSchema):
    purchase_order_id: Optional[str] = None
    item_no: Optional[int] = None
    service_code: Optional[str] = None
    sp_code: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    unit_of_measure: Optional[str] = None
    unit_price: Optional[float] = None
    extented_price: Optional[float] = None
    tax: Optional[float] = None
    discounts: Optional[float] = None
    
class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    purchase_order_id: Optional[str] = None
    item_no: Optional[int] = None
    service_code: Optional[str] = None
    sp_code: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    unit_of_measure: Optional[str] = None
    unit_price: Optional[float] = None
    extented_price: Optional[float] = None
    tax: Optional[float] = None
    discounts: Optional[float] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }


class PurchaseOrderItemUpdate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItemResponse(PurchaseOrderItemBase):
    id: str

    class Config:
        from_attributes = True

class PurchaseOrderItemView(PurchaseOrderItemResponse):
    pass
  
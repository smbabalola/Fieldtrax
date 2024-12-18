#delivery_ticket
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class DeliveryTicketItemBase(TimeStampSchema):
    
    delivery_ticket_id: str
    material_type: str
    item_no: int
    stock_no: int
    description: str
    kit_no: Optional[str] = None

class DeliveryTicketItemCreate(DeliveryTicketItemBase):
    delivery_ticket_id: str
    material_type: str
    item_no: int
    stock_no: int
    description: str
    kit_no: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
class DeliveryTicketItemUpdate(DeliveryTicketItemBase):
    delivery_ticket_id: str
    material_type: str
    item_no: int
    stock_no: int
    description: str
    kit_no: Optional[str] = None

class DeliveryTicketItemResponse(DeliveryTicketItemBase):
    id: str

    class Config:
        from_attributes = True

class DeliveryTicketItemView(DeliveryTicketItemResponse):
    pass
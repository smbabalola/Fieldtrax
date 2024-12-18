from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

#delivery_ticket
class DeliveryTicketBase(TimeStampSchema):
    wellbore_id: str
    ticket_number: str
    delivery_date: datetime
    supplier: str
    total_amount: float
    currency: Optional[str] = None
    received_by: str
    status: Optional[str] = None

class DeliveryTicketCreate(DeliveryTicketBase):
    wellbore_id: str
    ticket_number: str
    delivery_date: datetime
    supplier: str
    total_amount: float
    currency: Optional[str] = None
    received_by: str
    status: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
class DeliveryTicketUpdate(DeliveryTicketBase):
    wellbore_id: str
    ticket_number: str
    delivery_date: datetime
    supplier: str
    total_amount: float
    currency: Optional[str] = None
    received_by: str
    status: Optional[str] = None

class DeliveryTicketResponse(DeliveryTicketBase):
    id: str

    class Config:
        from_attributes = True

class DeliveryTicketView(DeliveryTicketResponse):
    pass
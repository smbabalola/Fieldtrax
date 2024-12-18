# File: app/schemas/jobsystem/purchase_order.py
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
from app.models.base import TimeStampSchema

class PurchaseOrderBase(TimeStampSchema):
    well_id: str = Field(..., max_length=50)
    po_number: str = Field(..., max_length=50)
    contract_no: Optional[str] = Field(None, max_length=50)
    vendor_no: Optional[str] = Field(None, max_length=50)
    DRSS_no: Optional[str] = Field(None, max_length=50)
    po_date: datetime
    supplier_name: Optional[str] = Field(None, max_length=100)
    supplier_address1: Optional[str] = Field(None, max_length=100)
    supplier_address2: Optional[str] = Field(None, max_length=100)
    county: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=50)
    supplier_contact: Optional[str] = Field(None, max_length=100)
    supplier_contact_information: Optional[str] = Field(None, max_length=100)
    buyer_name: Optional[str] = Field(None, max_length=100)
    buyer_address1: Optional[str] = Field(None, max_length=100)
    buyer_address_2: Optional[str] = Field(None, max_length=100)
    buyer_contact_information: Optional[str] = Field(None, max_length=100)
    delievry_address1: Optional[str] = Field(None, max_length=100)
    delivery_address2: Optional[str] = Field(None, max_length=100)
    delievry_postcode: Optional[str] = Field(None, max_length=20)
    delivery_zipcode: Optional[str] = Field(None, max_length=20)
    payment_terms: Optional[str] = Field(None, max_length=100)
    shipping_terms: Optional[str] = Field(None, max_length=100)

    @field_validator('po_date')
    @classmethod
    def validate_po_date(cls, v: datetime) -> datetime:
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    return datetime.fromisoformat(v.replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError("Invalid datetime format")
        return v

    model_config = ConfigDict(from_attributes=True)

class PurchaseOrderCreate(PurchaseOrderBase):
    well_id: str = Field(..., max_length=50)
    po_number: str = Field(..., max_length=50)
    contract_no: Optional[str] = Field(None, max_length=50)
    vendor_no: Optional[str] = Field(None, max_length=50)
    DRSS_no: Optional[str] = Field(None, max_length=50)
    po_date: datetime
    supplier_name: Optional[str] = Field(None, max_length=100)
    supplier_address1: Optional[str] = Field(None, max_length=100)
    supplier_address2: Optional[str] = Field(None, max_length=100)
    county: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=50)
    supplier_contact: Optional[str] = Field(None, max_length=100)
    supplier_contact_information: Optional[str] = Field(None, max_length=100)
    buyer_name: Optional[str] = Field(None, max_length=100)
    buyer_address1: Optional[str] = Field(None, max_length=100)
    buyer_address_2: Optional[str] = Field(None, max_length=100)
    buyer_contact_information: Optional[str] = Field(None, max_length=100)
    delievry_address1: Optional[str] = Field(None, max_length=100)
    delivery_address2: Optional[str] = Field(None, max_length=100)
    delievry_postcode: Optional[str] = Field(None, max_length=20)
    delivery_zipcode: Optional[str] = Field(None, max_length=20)
    payment_terms: Optional[str] = Field(None, max_length=100)
    shipping_terms: Optional[str] = Field(None, max_length=100)

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
    )
    
class PurchaseOrderUpdate(PurchaseOrderBase):
    pass

class PurchaseOrderResponse(PurchaseOrderBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
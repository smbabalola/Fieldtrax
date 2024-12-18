#contractor.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.base import TimeStampSchema


class ContractorBase(TimeStampSchema):
    contractor_name: str
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    post_code: Optional[str] = None
    zipcode: Optional[str] = None
    phone_no_1: Optional[str] = None
    phone_no_2: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

class ContractorCreate(ContractorBase):
    contractor_name: str
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    post_code: Optional[str] = None
    zipcode: Optional[str] = None
    phone_no_1: Optional[str] = None
    phone_no_2: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class ContractorUpdate(ContractorBase):
    contractor_name: str
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    post_code: Optional[str] = None
    zipcode: Optional[str] = None
    phone_no_1: Optional[str] = None
    phone_no_2: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

class ContractorResponse(ContractorBase):
    id: str

    class Config:
        from_attributes = True

class ContractorView(ContractorResponse):
    pass

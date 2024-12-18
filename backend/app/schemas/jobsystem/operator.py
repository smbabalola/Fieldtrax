#Operators
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class OperatorBase(TimeStampSchema):
    operator_name: str
    company_code: str
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    post_code: Optional[str] = None
    zipcode: Optional[str] = None
    phone_no_1: Optional[str] = None
    phone_no_2: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    
class OperatorCreate(OperatorBase):
    operator_name: str
    company_code: str
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
        
class OperatorUpdate(OperatorBase):
    pass

class OperatorResponse(OperatorBase):
    id: str

    class Config:
        from_attributes = True

class OperatorView(OperatorResponse):
    pass
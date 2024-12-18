from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class ContractTypeBase(TimeStampSchema):
    
    contract_type: Optional[str] = None
    description: Optional[str] = None
    

class ContractTypeCreate(ContractTypeBase):
    contract_type: Optional[str] = None
    description: Optional[str] = None
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class ContractTypeUpdate(ContractTypeBase):
    pass

class ContractTypeResponse(ContractTypeBase):
    id: str

    class Config:
        from_attributes = True

class ContractTypeView(ContractTypeResponse):
    pass
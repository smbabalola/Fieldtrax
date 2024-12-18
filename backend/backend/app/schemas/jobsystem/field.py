from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema
#field
class FieldBase(TimeStampSchema):
    
    field_name: str
    lease_name: str
    country: Optional[str] = None
    state: Optional[str] = None
    area: Optional[str] = None
	# [updated_by] [nvarchar](50) NULL,
    # date_last_updated: Optional[str] = None
    

class FieldCreate(FieldBase):
    field_name: str
    lease_name: str
    country: Optional[str] = None
    state: Optional[str] = None
    area: Optional[str] = None
	# [updated_by] [nvarchar](50) NULL,
    # date_last_updated: Optional[str] = None    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class FieldUpdate(FieldBase):
    pass

class FieldResponse(FieldBase):
    id: str

    class Config:
        from_attributes = True

class FieldView(FieldResponse):
    pass

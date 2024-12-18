#tubular
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class TubularBase(TimeStampSchema):
    tubulartype_id: str
    outer_diameter: Optional[float] = None
    inner_diameter: Optional[float] = None
    weight: Optional[float] = None
    yield_strength: Optional[float] = None
    capacity: Optional[float] = None
    volume: Optional[float] = None
    thread: Optional[str] = None
    burst: Optional[float] = None
    collapse: Optional[float] = None
    drift: Optional[float] = None
    oh_diameter: Optional[float] = None
    liner_Overlap: Optional[float] = None
    start_depth: Optional[float] = None
    end_depth: Optional[float] = None
    liner_top_depth: Optional[str] = None

class TubularCreate(TubularBase):
    tubulartype_id: str
    outer_diameter: Optional[float] = None
    inner_diameter: Optional[float] = None
    weight: Optional[float] = None
    yield_strength: Optional[float] = None
    capacity: Optional[float] = None
    volume: Optional[float] = None
    thread: Optional[str] = None
    burst: Optional[float] = None
    collapse: Optional[float] = None
    drift: Optional[float] = None
    oh_diameter: Optional[float] = None
    liner_Overlap: Optional[float] = None
    start_depth: Optional[float] = None
    end_depth: Optional[float] = None
    liner_top_depth: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
        
class TubularUpdate(TubularBase):
    pass

class TubularResponse(TubularBase):
    id: str

    class Config:
        from_attributes = True

class TubularView(TubularResponse):
    pass

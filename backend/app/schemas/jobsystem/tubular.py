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
    grade: Optional[str] = None
    thread: Optional[str] = None
    open_hole_size: Optional[float] = None
    yield_strength: Optional[float] = None
    capacity: Optional[float] = None
    volume: Optional[float] = None
    burst: Optional[float] = None
    collapse: Optional[float] = None
    drift: Optional[float] = None
    liner_Overlap: Optional[float] = None
    start_depth: Optional[float] = None
    end_depth: Optional[float] = None
    remarks: Optional[str] = None

class TubularCreate(TubularBase):
    tubulartype_id: str
    outer_diameter: Optional[float] = None
    inner_diameter: Optional[float] = None
    weight: Optional[float] = None
    grade: Optional[str] = None
    thread: Optional[str] = None
    open_hole_size: Optional[float] = None
    yield_strength: Optional[float] = None
    capacity: Optional[float] = None
    volume: Optional[float] = None
    burst: Optional[float] = None
    collapse: Optional[float] = None
    drift: Optional[float] = None
    liner_Overlap: Optional[float] = None
    start_depth: Optional[float] = None
    end_depth: Optional[float] = None
    remarks: Optional[str] = None
    
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

class CasingCreate(TubularCreate):
    cement_top: Optional[float] = None
    cement_yield: Optional[float] = None
    tubulartype_id: str 

class CasingUpdate(TubularUpdate):
    cement_top: Optional[float] = None
    cement_yield: Optional[float] = None

class CasingResponse(TubularResponse):
    cement_top: Optional[float] = None
    cement_yield: Optional[float] = None
    
class CasingView(TubularResponse):
    pass

class LinerCreate(TubularCreate):
    liner_top: Optional[float] = None
    liner_bottom: Optional[float] = None
    tubulartype_id: str 

class LinerUpdate(TubularUpdate):
    liner_top: Optional[float] = None
    liner_bottom: Optional[float] = None

class LinerResponse(TubularResponse):
    liner_top: Optional[float] = None
    liner_bottom: Optional[float] = None
    
class LinerView(TubularResponse):
    pass

class DrillstringCreate(TubularCreate):
    component_type: Optional[str] = None
    tubulartype_id: str 

class DrillstringUpdate(TubularUpdate):
    component_type: Optional[str] = None

class DrillstringResponse(TubularResponse):
    component_type: Optional[str] = None

class DrillingView(TubularResponse):
    pass
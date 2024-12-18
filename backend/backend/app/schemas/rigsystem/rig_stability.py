from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class RigStabilityBase(TimeStampSchema):
    rig_id: str
    max_deck_load_op_draft: Optional[float] = None
    max_deck_load_survival_draft: Optional[float] = None
    max_deck_load_transit_draft: Optional[float] = None
    max_deck_load_water_depth: Optional[float] = None
    number_thrusters: Optional[float] = None
    thruster_power: Optional[float] = None
    number_anchors: Optional[int] = None
    number_riser_tensioners: Optional[int] = None
    number_guideline_tensioners: Optional[int] = None
    
class RigStabilityCreate(RigStabilityBase):
    pass

class RigStabilityUpdate(RigStabilityBase):
    pass

class RigStabilityResponse(RigStabilityBase):
    id: str

    class Config:
        from_attributes = True

class RigStabilityView(RigStabilityResponse):
    pass
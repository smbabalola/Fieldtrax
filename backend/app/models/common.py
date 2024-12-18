# app/models/common.py
from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class CoordinateSystem(str, Enum):
    UTM = "UTM"
    GEOGRAPHIC = "GEOGRAPHIC"
    LOCAL_GRID = "LOCAL_GRID"

class ReferencePoint(str, Enum):
    SLOT = "SLOT"
    FACILITY = "FACILITY"
    PLATFORM = "PLATFORM"
    SURFACE_LOCATION = "SURFACE_LOCATION"

class WellboreType(str, Enum):
    ORIGINAL = "ORIGINAL"
    SIDETRACK = "SIDETRACK"
    MULTILATERAL = "MULTILATERAL"
    BYPASS = "BYPASS"

class CasingType(str, Enum):
    CONDUCTOR = "CONDUCTOR"
    SURFACE = "SURFACE"
    INTERMEDIATE = "INTERMEDIATE"
    PRODUCTION = "PRODUCTION"
    LINER = "LINER"
    
class FieldLocation(str, Enum):
    BARGE = "BARGE"
    DEEPWATER = "DEEPWATER"
    LAND = "LAND"
    SHELF = "SHELF"
    
class Spacer(str, Enum):
    BASEOIL = "BASEOIL"
    MUD = "MUD"
    MUDPUSH = "MUDPUSH"
    OTHER = "OTHER"
    WATER = "WATER"
    
    
class WellType(str, Enum):
    DEVIATED = "DEVIATED"
    DISPOSAL = "DISPOSAL"
    EXTENDEDREACH = "EXTENDED REACH"
    HORIZONTAL = "HORIZONTAL"
    INJECTOR = "INJECTOR"
    REENTRY = "REENTRY"
    VERTICAL = "VERTICAL"
    WORKOVER = "WORKOVER"
    OIL = "OIL"
    EXPLORATION = "EXPLORATION"
    GAS = "GAS"
    SELECTIVEWATERINJECTOR = "SELECTIVEWATERINJECTOR"
    COILEDTUBINGDRILLING = "COILEDTUBINGDRILLING"

class JobStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"

class RigType(str, Enum):
    LAND = "land"
    OFFSHORE = "offshore"
    PLATFORM = "platform"

class FluidType(str, Enum):
    WATER = "water"
    OIL = "oil"
    MUD = "mud"
    BRINE = "brine"    

class BaseModelWithTimestamp(BaseModel):
    """Base model with timestamp fields"""
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    modified_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(from_attributes=True)

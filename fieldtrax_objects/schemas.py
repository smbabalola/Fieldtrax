from datetime import date
from pydantic import BaseModel, field_validator, validator
from enum import Enum

class Pump_Types(Enum):
    TRIPLEX = 'triplex'
    DUPLEX = 'duplex'

class Genre_Types(Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip-hop'
    GRUNGE = 'grunge'
    PROGRESSIVE_ROCK = 'progressive rock'
    ROCK_AND_ROLL = 'rock and roll'
    THRASH_METAL = 'thrash metal'
    HARD_ROCK = 'hard rock'

class Genre_Options(Enum):
    ROCK = 'Rock'
    ELECTRONIC = 'Electronic'
    METAL = 'Metal'
    HIP_HOP = 'Hip-Hop'
    GRUNGE = 'Grunge'
    PROGRESSIVE_ROCK = 'Progressive Rock'
    ROCK_AND_ROLL = 'Rock and Roll'
    THRASH_METAL = 'Thrash Metal'
    HARD_ROCK = "Hard Rock"


class Pump(BaseModel):
    id: int
    rig_id: int
    rig_name: str
    liner_id: float
    pump_type: str
    stroke_length: float
    rod_diameter: float
    efficiency: float
    riser: bool
    kill: bool
    
class Rig(BaseModel):
    id: int
    rig_id: str
    rig_name: str
    rig_pumps: list[Pump] = []
    
class Album(BaseModel):
    title: str
    release_date: date
    
class BandBase(BaseModel):
    name: str
    genre: Genre_Options
    albums: list[Album] = []
    
class BandCreate(BandBase):
    @field_validator("genre", mode="before")
    def title_case_genre(cls, value):
        return value.title()

class BandwithID(BandBase):
    id: int
    
    
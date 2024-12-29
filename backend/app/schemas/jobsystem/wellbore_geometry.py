from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

from app.models.base import TimeStampSchema

class WellboreGeometryBase(TimeStampSchema):
    wellbore_id: str # link to wellbore table
    tubular_id: str # link to tubular table

class WellboreGeometryCreate(WellboreGeometryBase):
    wellbore_id: str
    tubular_id: str 

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }



class WellboreGeometryUpdate(WellboreGeometryBase):
    pass

class WellboreGeometryResponse(WellboreGeometryBase):
    id: str

    class Config:
        from_attributes = True

class WellboreGeometryView(WellboreGeometryResponse):
    pass

#Example usage
if __name__ == "__main__":
    wellbore_geometry_data = {
        "name": "Test Wellbore Geometry",
        "wellbore_id": 1
    }

    wellbore_geometry_create = WellboreGeometryCreate(**wellbore_geometry_data)
    print(wellbore_geometry_create.model_dump_json(indent=2))

    wellbore_geometry_response = WellboreGeometryResponse(id=1, **wellbore_geometry_data)
    print(wellbore_geometry_response.model_dump_json(indent=2))

    try:
        invalid_wellbore_geometry_data = {
            "name": "", # invalid name
            "wellbore_id": -1 # invalid wellbore_id
        }
        WellboreGeometryCreate(**invalid_wellbore_geometry_data)
    except ValueError as e:
        print(f"Validation error: {e}")
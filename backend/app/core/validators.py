# app/core/validators.py
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, validator, Field
from uuid import UUID

class EnhancedJobValidation(BaseModel):
    """Enhanced validation rules for job operations"""
    
    @validator('spuddate')
    def validate_spuddate(cls, v):
        if v > datetime.utcnow():
            raise ValueError("Spud date cannot be in the future")
        return v

    @validator('waterdepth')
    def validate_waterdepth(cls, v):
        if v and v.value < 0:
            raise ValueError("Water depth cannot be negative")
        if v and v.value > 12000:  # Example maximum depth
            raise ValueError("Water depth exceeds maximum allowed value")
        return v

    @validator('well_name')
    def validate_well_name(cls, v):
        if not v.strip():
            raise ValueError("Well name cannot be empty")
        if len(v) > 100:
            raise ValueError("Well name is too long")
        return v.strip()

class FluidValidation(BaseModel):
    """Enhanced validation for fluid operations"""
    
    @validator('density')
    def validate_density(cls, v):
        if v.value <= 0:
            raise ValueError("Density must be positive")
        if v.unit == "ppg" and v.value > 24:  # Example maximum mud weight
            raise ValueError("Density exceeds maximum allowed value")
        return v

    @validator('viscosity')
    def validate_viscosity(cls, v):
        if v and v.value < 0:
            raise ValueError("Viscosity cannot be negative")
        return v

class TallyValidation(BaseModel):
    """Enhanced validation for tally operations"""
    
    @validator('items')
    def validate_tally_items(cls, v):
        if not v:
            raise ValueError("Tally must contain at least one item")
        
        total_length = 0
        for item in v:
            if item.length.value <= 0:
                raise ValueError("Tally item length must be positive")
            total_length += item.length.value
            
        if total_length > 25000:  # Example maximum total length
            raise ValueError("Total tally length exceeds maximum allowed value")
        return v


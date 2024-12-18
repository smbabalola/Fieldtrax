# app/models/gradients.py
from pydantic import BaseModel, Field
from typing import List, Optional
from ..core.units.quantity import Length, Pressure, Temperature

class PressurePoint(BaseModel):
    """Pressure gradient point model"""
    md: Length
    pressure_gradient: Pressure

class GradientProfile(BaseModel):
    """Base pressure gradient profile model"""
    points: List[PressurePoint] = Field(default_factory=list)
    
    def add_point(self, point: PressurePoint):
        self.points.append(point)
        self.points.sort(key=lambda x: x.md.value)

class CollapsePressureGradient(GradientProfile):
    """Collapse pressure gradient profile"""
    pass

class PorePressureGradient(GradientProfile):
    """Pore pressure gradient profile"""
    pass

class FracturePressureGradient(GradientProfile):
    """Fracture pressure gradient profile"""
    pass

class TemperaturePoint(BaseModel):
    """Temperature gradient point model"""
    tvd: Length
    temperature: Temperature
    gradient: Temperature  # Temperature gradient per unit length

class GeothermalGradient(BaseModel):
    """Geothermal gradient profile model"""
    points: List[TemperaturePoint] = Field(default_factory=list)
    
    def add_point(self, point: TemperaturePoint):
        self.points.append(point)
        self.points.sort(key=lambda x: x.tvd.value)

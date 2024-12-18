# app/core/units/models.py
from typing import Dict, Any, Type, Optional, get_args, get_origin
from pydantic import BaseModel, Field, validator, root_validator
from datetime import datetime
import inspect

from app.core.units.quantity import (
    PhysicalQuantity, Length, Depth, Volume, Weight, Pressure,
    Temperature, FlowRate, Density, Viscosity, Force, Energy,
    RPM, Torque, Area, Diameter, WeightPerLength, FluidVolume,
    DLS, Azimuth, MudWeight
)

class QuantityField(BaseModel):
    """Base model for handling physical quantities in Pydantic models."""
    value: float
    unit: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, PhysicalQuantity):
            return cls(value=v.value, unit=v.unit)
        elif isinstance(v, dict):
            return cls(**v)
        elif isinstance(v, (int, float)):
            # Use default unit if only value is provided
            quantity_class = cls.get_quantity_class()
            default_unit = quantity_class._default_unit
            return cls(value=float(v), unit=default_unit)
        raise ValueError(f'Invalid value type for {cls.__name__}')

    @classmethod
    def get_quantity_class(cls) -> Type[PhysicalQuantity]:
        """Get the corresponding PhysicalQuantity class."""
        raise NotImplementedError("Subclasses must implement get_quantity_class")

    def to_quantity(self) -> PhysicalQuantity:
        """Convert to PhysicalQuantity instance."""
        quantity_class = self.get_quantity_class()
        return quantity_class(self.value, self.unit)

    class Config:
        json_encoders = {
            PhysicalQuantity: lambda v: {"value": v.value, "unit": v.unit}
        }

class LengthField(QuantityField):
    @classmethod
    def get_quantity_class(cls) -> Type[PhysicalQuantity]:
        return Length

    @validator('unit')
    def validate_unit(cls, v):
        if v not in Length._valid_units:
            raise ValueError(f'Invalid length unit: {v}')
        return v

class DepthField(QuantityField):
    @classmethod
    def get_quantity_class(cls) -> Type[PhysicalQuantity]:
        return Depth

    @validator('unit')
    def validate_unit(cls, v):
        if v not in Depth._valid_units:
            raise ValueError(f'Invalid depth unit: {v}')
        return v

class VolumeField(QuantityField):
    @classmethod
    def get_quantity_class(cls) -> Type[PhysicalQuantity]:
        return Volume

    @validator('unit')
    def validate_unit(cls, v):
        if v not in Volume._valid_units:
            raise ValueError(f'Invalid volume unit: {v}')
        return v

class WeightField(QuantityField):
    @classmethod
    def get_quantity_class(cls) -> Type[PhysicalQuantity]:
        return Weight

    @validator('unit')
    def validate_unit(cls, v):
        if v not in Weight._valid_units:
            raise ValueError(f'Invalid weight unit: {v}')
        return v

class PressureField(QuantityField):
    @classmethod
    def get_quantity_class(cls) -> Type[PhysicalQuantity]:
        return Pressure

    @validator('unit')
    def validate_unit(cls, v):
        if v not in Pressure._valid_units:
            raise ValueError(f'Invalid pressure unit: {v}')
        return v

class DensityField(QuantityField):
    @classmethod
    def get_quantity_class(cls) -> Type[PhysicalQuantity]:
        return Density

    @validator('unit')
    def validate_unit(cls, v):
        if v not in Density._valid_units:
            raise ValueError(f'Invalid density unit: {v}')
        return v

class ViscosityField(QuantityField):
    @classmethod
    def get_quantity_class(cls) -> Type[PhysicalQuantity]:
        return Viscosity

    @validator('unit')
    def validate_unit(cls, v):
        if v not in Viscosity._valid_units:
            raise ValueError(f'Invalid viscosity unit: {v}')
        return v

class RPMField(QuantityField):
    @classmethod
    def get_quantity_class(cls) -> Type[PhysicalQuantity]:
        return RPM

    @validator('unit')
    def validate_unit(cls, v):
        if v not in RPM._valid_units:
            raise ValueError(f'Invalid RPM unit: {v}')
        return v

# Now let's create model mixins to handle quantity fields
class QuantityMixin:
    """Mixin class to add quantity conversion methods to Pydantic models."""
    
    @classmethod
    def get_quantity_fields(cls) -> Dict[str, Type[QuantityField]]:
        """Get all quantity fields in the model."""
        fields = {}
        for name, field in cls.__fields__.items():
            if issubclass(field.type_, QuantityField):
                fields[name] = field.type_
        return fields

    def convert_quantities(self) -> Dict[str, PhysicalQuantity]:
        """Convert all quantity fields to PhysicalQuantity instances."""
        quantities = {}
        for name, field_type in self.get_quantity_fields().items():
            field_value = getattr(self, name)
            if field_value is not None:
                quantities[name] = field_value.to_quantity()
        return quantities

# Example of updated Pydantic models using the new fields
class Fluid(BaseModel, QuantityMixin):
    """Model for fluid-related information with physical quantities."""
    id: str
    job_id: str
    fluid_type: str
    volume: VolumeField
    density: DensityField
    viscosity: Optional[ViscosityField] = None
    description: str
    properties: Dict[str, float] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            PhysicalQuantity: lambda v: {"value": v.value, "unit": v.unit}
        }
        
    def calculate_hydrostatic_pressure(self, depth: Depth) -> Pressure:
        """Calculate hydrostatic pressure using proper quantity types."""
        density = self.density.to_quantity()
        return density.calculate_hydrostatic_pressure(depth)

class PhysicalBarrier(BaseModel, QuantityMixin):
    """Model for physical barriers with physical quantities."""
    id: str
    job_id: str
    barrier_type: str
    depth: DepthField
    length: Optional[LengthField] = None
    pressure_rating: PressureField
    installation_date: datetime
    installed_by: str
    verified_by: Optional[str] = None
    verification_date: Optional[datetime] = None

    def check_pressure_rating(self, applied_pressure: Pressure) -> bool:
        """Check if barrier can withstand applied pressure."""
        rating = self.pressure_rating.to_quantity()
        return applied_pressure.to_unit("psi") <= rating.to_unit("psi")

# Example of usage:
"""
# Create a fluid instance
fluid = Fluid(
    id="123",
    job_id="456",
    fluid_type="Drilling Mud",
    volume={"value": 100, "unit": "bbl"},
    density={"value": 12.5, "unit": "ppg"},
    viscosity={"value": 45, "unit": "cP"},
    description="KCl Polymer Mud"
)

# Access as quantities
quantities = fluid.convert_quantities()
volume = quantities["volume"]  # Volume instance
density = quantities["density"]  # Density instance

# Calculate hydrostatic pressure
depth = Depth(10000, "ft")
pressure = fluid.calculate_hydrostatic_pressure(depth)
print(f"Hydrostatic pressure: {pressure}")  # Will print in psi
"""
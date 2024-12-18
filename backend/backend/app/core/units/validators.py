# app/core/units/validators.py
from typing import Dict, List, Optional, Union, Tuple
from datetime import datetime
import math
from enum import Enum

from app.core.units.quantity import (
    Length, Depth, Volume, Weight, Pressure,
    Temperature, FlowRate, Density, Viscosity,
    Force, Energy, RPM, Torque, Area, Diameter,
    WeightPerLength, FluidVolume, DLS, Azimuth,
    MudWeight, PhysicalQuantity
)

class OperationalLimits(Enum):
    """Common operational limits for oil and gas operations."""
    MAX_DEPTH = 35000  # Maximum depth in feet
    MAX_PRESSURE = 15000  # Maximum pressure in psi
    MAX_TEMPERATURE = 350  # Maximum temperature in °F
    MAX_MUD_WEIGHT = 22  # Maximum mud weight in ppg
    MAX_DLS = 6  # Maximum dogleg severity in deg/100ft
    MIN_CASING_SAFETY_FACTOR = 1.2  # Minimum safety factor for casing design
    MAX_ECD = 19.5  # Maximum ECD in ppg
    MIN_ANNULAR_VELOCITY = 120  # Minimum annular velocity in ft/min
    MAX_ANNULAR_VELOCITY = 600  # Maximum annular velocity in ft/min
    MIN_SURGE_SAFETY_MARGIN = 0.5  # Minimum surge/swab safety margin in ppg

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class OperationalValidator:
    """Base class for operational validators."""
    
    @staticmethod
    def validate_within_range(
        value: float,
        min_value: float,
        max_value: float,
        parameter_name: str
    ) -> None:
        """Validate if a value is within an acceptable range."""
        if not min_value <= value <= max_value:
            raise ValidationError(
                f"{parameter_name} value {value} is outside acceptable range "
                f"[{min_value}, {max_value}]"
            )

class DepthValidator(OperationalValidator):
    """Validator for depth-related measurements."""
    
    @staticmethod
    def validate_depth(depth: Depth) -> None:
        """Validate if depth is within operational limits."""
        depth_ft = depth.to_unit("ft")
        OperationalValidator.validate_within_range(
            depth_ft,
            0,
            OperationalLimits.MAX_DEPTH.value,
            "Depth"
        )
    
    @staticmethod
    def validate_casing_setting_depth(
        depth: Depth,
        pressure_gradient: float,
        safety_factor: float = OperationalLimits.MIN_CASING_SAFETY_FACTOR.value
    ) -> None:
        """Validate casing setting depth based on pressure gradient."""
        depth_ft = depth.to_unit("ft")
        max_safe_depth = (OperationalLimits.MAX_PRESSURE.value / pressure_gradient) * safety_factor
        
        if depth_ft > max_safe_depth:
            raise ValidationError(
                f"Casing setting depth {depth_ft} ft exceeds maximum safe depth "
                f"{max_safe_depth:.0f} ft for given pressure gradient"
            )

class PressureValidator(OperationalValidator):
    """Validator for pressure-related measurements."""
    
    @staticmethod
    def validate_pressure(pressure: Pressure) -> None:
        """Validate if pressure is within operational limits."""
        pressure_psi = pressure.to_unit("psi")
        OperationalValidator.validate_within_range(
            pressure_psi,
            0,
            OperationalLimits.MAX_PRESSURE.value,
            "Pressure"
        )
    
    @staticmethod
    def validate_pressure_integrity(
        test_pressure: Pressure,
        formation_strength: Pressure,
        safety_factor: float = 0.9
    ) -> None:
        """Validate pressure test against formation strength."""
        test_psi = test_pressure.to_unit("psi")
        strength_psi = formation_strength.to_unit("psi")
        max_test_pressure = strength_psi * safety_factor
        
        if test_psi > max_test_pressure:
            raise ValidationError(
                f"Test pressure {test_psi} psi exceeds maximum safe pressure "
                f"{max_test_pressure:.0f} psi"
            )

class MudWeightValidator(OperationalValidator):
    """Validator for mud weight and ECD."""
    
    @staticmethod
    def validate_mud_weight(mud_weight: MudWeight) -> None:
        """Validate if mud weight is within operational limits."""
        weight_ppg = mud_weight.to_unit("ppg")
        OperationalValidator.validate_within_range(
            weight_ppg,
            8.33,  # Water density
            OperationalLimits.MAX_MUD_WEIGHT.value,
            "Mud Weight"
        )
    
    @staticmethod
    def validate_ecd(
        ecd: MudWeight,
        fracture_gradient: Pressure,
        pore_pressure: Pressure,
        depth: Depth
    ) -> None:
        """Validate ECD against fracture and pore pressure gradients."""
        ecd_ppg = ecd.to_unit("ppg")
        depth_ft = depth.to_unit("ft")
        
        # Calculate pressure gradients in ppg
        frac_ppg = (fracture_gradient.to_unit("psi") / depth_ft) / 0.052
        pore_ppg = (pore_pressure.to_unit("psi") / depth_ft) / 0.052
        
        if ecd_ppg > frac_ppg:
            raise ValidationError(
                f"ECD {ecd_ppg:.2f} ppg exceeds fracture gradient {frac_ppg:.2f} ppg"
            )
        
        if ecd_ppg < pore_ppg + OperationalLimits.MIN_SURGE_SAFETY_MARGIN.value:
            raise ValidationError(
                f"ECD {ecd_ppg:.2f} ppg provides insufficient overbalance to "
                f"pore pressure {pore_ppg:.2f} ppg"
            )

class HydraulicsValidator(OperationalValidator):
    """Validator for hydraulics calculations."""
    
    @staticmethod
    def validate_flow_rate(
        flow_rate: FlowRate,
        hole_size: Diameter,
        pipe_size: Diameter
    ) -> None:
        """Validate flow rate for adequate hole cleaning."""
        # Calculate annular velocity
        hole_area = math.pi * (hole_size.to_unit("in")**2 - pipe_size.to_unit("in")**2) / 4
        flow_gpm = flow_rate.to_unit("gpm")
        velocity_ft_min = (flow_gpm * 144) / (hole_area * 7.48052)
        
        OperationalValidator.validate_within_range(
            velocity_ft_min,
            OperationalLimits.MIN_ANNULAR_VELOCITY.value,
            OperationalLimits.MAX_ANNULAR_VELOCITY.value,
            "Annular Velocity"
        )
    
    @staticmethod
    def validate_pump_pressure(
        pressure: Pressure,
        pump_rating: Pressure,
        safety_factor: float = 0.9
    ) -> None:
        """Validate pump pressure against pump rating."""
        pressure_psi = pressure.to_unit("psi")
        max_pressure = pump_rating.to_unit("psi") * safety_factor
        
        if pressure_psi > max_pressure:
            raise ValidationError(
                f"Pump pressure {pressure_psi} psi exceeds maximum safe pressure "
                f"{max_pressure:.0f} psi"
            )

class DirectionalValidator(OperationalValidator):
    """Validator for directional drilling parameters."""
    
    @staticmethod
    def validate_dogleg_severity(dls: DLS) -> None:
        """Validate dogleg severity."""
        severity = dls.to_unit("deg/100ft")
        OperationalValidator.validate_within_range(
            severity,
            0,
            OperationalLimits.MAX_DLS.value,
            "Dogleg Severity"
        )
    
    @staticmethod
    def validate_build_rate(
        build_rate: float,
        tool_capability: float,
        safety_factor: float = 0.9
    ) -> None:
        """Validate build rate against tool capabilities."""
        max_build_rate = tool_capability * safety_factor
        
        if build_rate > max_build_rate:
            raise ValidationError(
                f"Build rate {build_rate} deg/100ft exceeds tool capability "
                f"{max_build_rate:.1f} deg/100ft"
            )

class TemperatureValidator(OperationalValidator):
    """Validator for temperature-related measurements."""
    
    @staticmethod
    def validate_temperature(temperature: Temperature) -> None:
        """Validate if temperature is within operational limits."""
        temp_f = temperature.to_unit("F")
        OperationalValidator.validate_within_range(
            temp_f,
            32,  # Freezing point
            OperationalLimits.MAX_TEMPERATURE.value,
            "Temperature"
        )
    
    @staticmethod
    def validate_equipment_rating(
        temperature: Temperature,
        equipment_rating: Temperature,
        safety_margin: float = 25  # °F
    ) -> None:
        """Validate temperature against equipment rating."""
        temp_f = temperature.to_unit("F")
        rating_f = equipment_rating.to_unit("F")
        
        if temp_f > (rating_f - safety_margin):
            raise ValidationError(
                f"Temperature {temp_f}°F too close to equipment rating {rating_f}°F"
            )

class WeightValidator(OperationalValidator):
    """Validator for weight-related measurements."""
    
    @staticmethod
    def validate_hook_load(
        hook_load: Weight,
        rig_capacity: Weight,
        safety_factor: float = 0.8
    ) -> None:
        """Validate hook load against rig capacity."""
        load_klb = hook_load.to_unit("klbf")
        max_load = rig_capacity.to_unit("klbf") * safety_factor
        
        if load_klb > max_load:
            raise ValidationError(
                f"Hook load {load_klb} klb exceeds safe working load "
                f"{max_load:.0f} klb"
            )
    
    @staticmethod
    def validate_string_weight(
        string_weight: Weight,
        tensile_rating: Weight,
        safety_factor: float = 1.3
    ) -> None:
        """Validate string weight against tensile rating."""
        weight_lb = string_weight.to_unit("lbf")
        max_weight = tensile_rating.to_unit("lbf") / safety_factor
        
        if weight_lb > max_weight:
            raise ValidationError(
                f"String weight {weight_lb} lbf exceeds safe working load "
                f"{max_weight:.0f} lbf"
            )

def validate_quantity_combination(
    quantities: Dict[str, PhysicalQuantity],
    validation_func: callable,
    error_message: str
) -> None:
    """Generic function to validate a combination of quantities."""
    try:
        validation_func(**quantities)
    except Exception as e:
        raise ValidationError(f"{error_message}: {str(e)}")

# Example usage:
"""
# Validate depth
depth = Depth(15000, "ft")
try:
    DepthValidator.validate_depth(depth)
    print("Depth is within operational limits")
except ValidationError as e:
    print(f"Depth validation failed: {e}")

# Validate mud weight and ECD
mud_weight = MudWeight(12.5, "ppg")
depth = Depth(10000, "ft")
fracture_pressure = Pressure(8000, "psi")
pore_pressure = Pressure(4000, "psi")

try:
    MudWeightValidator.validate_mud_weight(mud_weight)
    MudWeightValidator.validate_ecd(
        mud_weight,
        fracture_pressure,
        pore_pressure,
        depth
    )
    print("Mud weight and ECD are within safe limits")
except ValidationError as e:
    print(f"Mud weight validation failed: {e}")

# Validate flow rate for hole cleaning
flow_rate = FlowRate(500, "gpm")
hole_size = Diameter(8.5, "in")
pipe_size = Diameter(5.0, "in")

try:
    HydraulicsValidator.validate_flow_rate(flow_rate, hole_size, pipe_size)
    print("Flow rate provides adequate hole cleaning")
except ValidationError as e:
    print(f"Flow rate validation failed: {e}")
"""
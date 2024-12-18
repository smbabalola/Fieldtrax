# app/core/units/utils.py
from typing import Dict, List, Tuple, Optional, Type, Union
from datetime import datetime
import math

from app.core.units.quantity import (
    Length, Depth, Velocity, Volume, Weight, Pressure,
    Temperature, FlowRate, Density, Viscosity,
    Force, Energy, RPM, Torque, Area, Diameter,
    WeightPerLength, FluidVolume, DLS, Azimuth,
    MudWeight, PhysicalQuantity
)

class HydraulicsCalculator:
    """Utility class for hydraulics calculations."""
    
    @staticmethod
    def calculate_ecd(
        static_mud_weight: MudWeight,
        annular_pressure: Pressure,
        true_vertical_depth: Depth
    ) -> MudWeight:
        """Calculate Equivalent Circulating Density (ECD)."""
        # ECD = Static MW + (Annular Pressure / (0.052 * TVD))
        static_ppg = static_mud_weight.to_unit("ppg")
        pressure_psi = annular_pressure.to_unit("psi")
        depth_ft = true_vertical_depth.to_unit("ft")
        
        additional_density = pressure_psi / (0.052 * depth_ft)
        return MudWeight(static_ppg + additional_density, "ppg")
    
    @staticmethod
    def calculate_annular_velocity(
        flow_rate: FlowRate,
        hole_size: Diameter,
        pipe_size: Diameter
    ) -> Velocity:
        """Calculate annular velocity."""
        # Convert to consistent units
        flow_gpm = flow_rate.to_unit("gpm")
        hole_id = hole_size.to_unit("in")
        pipe_od = pipe_size.to_unit("in")
        
        # Calculate annular area in square inches
        annular_area = math.pi * (hole_id**2 - pipe_od**2) / 4
        
        # Calculate velocity in ft/min
        velocity = (flow_gpm * 144) / (annular_area * 7.48052)
        return Velocity(velocity, "ft/min")
    
    @staticmethod
    def pressure_loss_pipe(
        flow_rate: FlowRate,
        pipe_length: Length,
        pipe_id: Diameter,
        fluid_density: Density,
        fluid_viscosity: Viscosity
    ) -> Pressure:
        """Calculate pressure loss in pipe using Fanning friction factor."""
        # Convert to consistent units
        q = flow_rate.to_unit("ft3/s")
        l = pipe_length.to_unit("ft")
        d = pipe_id.to_unit("ft")
        rho = fluid_density.to_unit("lb/ft3")
        mu = fluid_viscosity.to_unit("lb.s/ft2")
        
        # Calculate Reynolds number
        velocity = (4 * q) / (math.pi * d**2)
        re = (rho * velocity * d) / mu
        
        # Calculate friction factor
        if re < 2100:  # Laminar flow
            f = 16 / re
        else:  # Turbulent flow (using approximate Blasius equation)
            f = 0.0791 / (re**0.25)
        
        # Calculate pressure loss
        dp = (2 * f * rho * velocity**2 * l) / d
        return Pressure(dp / 144, "psi")  # Convert psf to psi

class WellboreGeometry:
    """Utility class for wellbore geometry calculations."""
    
    @staticmethod
    def calculate_displacement(
        md: Depth,
        inc: float,
        azi: float
    ) -> Tuple[Length, Length, Depth]:
        """Calculate TVD, Northing, and Easting from MD, Inclination, and Azimuth."""
        # Using average angle method
        tvd = Depth(md.value * math.cos(math.radians(inc)), md.unit)
        horizontal = Length(md.value * math.sin(math.radians(inc)), md.unit)
        
        north = Length(horizontal.value * math.cos(math.radians(azi)), horizontal.unit)
        east = Length(horizontal.value * math.sin(math.radians(azi)), horizontal.unit)
        
        return (north, east, tvd)
    
    @staticmethod
    def dogleg_severity(
        inc1: float,
        azi1: float,
        inc2: float,
        azi2: float,
        course_length: Length
    ) -> DLS:
        """Calculate Dogleg Severity between two survey points."""
        # Convert angles to radians
        inc1_rad = math.radians(inc1)
        inc2_rad = math.radians(inc2)
        azi1_rad = math.radians(azi1)
        azi2_rad = math.radians(azi2)
        
        # Calculate dogleg angle
        cos_dl = (
            math.cos(inc1_rad) * math.cos(inc2_rad) +
            math.sin(inc1_rad) * math.sin(inc2_rad) *
            math.cos(azi2_rad - azi1_rad)
        )
        
        if cos_dl > 1:  # Handle floating point errors
            cos_dl = 1
            
        dogleg = math.degrees(math.acos(cos_dl))
        
        # Calculate DLS in degrees per 100 ft
        length_ft = course_length.to_unit("ft")
        dls = (dogleg * 100) / length_ft
        
        return DLS(dls, "deg/100ft")

class VolumeCalculator:
    """Utility class for volume calculations."""
    
    @staticmethod
    def annular_capacity(
        hole_size: Diameter,
        pipe_size: Diameter
    ) -> float:
        """Calculate annular capacity in bbl/ft."""
        hole_id = hole_size.to_unit("in")
        pipe_od = pipe_size.to_unit("in")
        
        capacity = (hole_id**2 - pipe_od**2) / 1029.4
        return capacity
    
    @staticmethod
    def displacement_volume(
        length: Length,
        pipe_size: Diameter
    ) -> Volume:
        """Calculate volume displaced by pipe."""
        l_ft = length.to_unit("ft")
        d_in = pipe_size.to_unit("in")
        
        vol_bbl = (d_in**2 * l_ft) / 1029.4
        return Volume(vol_bbl, "bbl")
    
    @staticmethod
    def calculate_bottoms_up_time(
        hole_size: Diameter,
        pipe_size: Diameter,
        depth: Depth,
        flow_rate: FlowRate
    ) -> float:
        """Calculate time to complete one full circulation (bottoms up)."""
        capacity = VolumeCalculator.annular_capacity(hole_size, pipe_size)
        depth_ft = depth.to_unit("ft")
        flow_bpm = flow_rate.to_unit("bpm")
        
        annular_volume = capacity * depth_ft
        return annular_volume / flow_bpm  # Returns time in minutes

class PressureCalculator:
    """Utility class for pressure calculations."""
    
    @staticmethod
    def hydrostatic_pressure(
        mud_weight: MudWeight,
        depth: Depth
    ) -> Pressure:
        """Calculate hydrostatic pressure."""
        ppg = mud_weight.to_unit("ppg")
        ft = depth.to_unit("ft")
        
        pressure = 0.052 * ppg * ft
        return Pressure(pressure, "psi")
    
    @staticmethod
    def fracture_pressure(
        depth: Depth,
        pore_pressure: Pressure,
        poisson_ratio: float = 0.25,
        overburden_gradient: float = 1.0
    ) -> Pressure:
        """Calculate fracture pressure using modified Hubbert-Willis method."""
        tvd = depth.to_unit("ft")
        pp_psi = pore_pressure.to_unit("psi")
        
        # Calculate overburden pressure
        ob_pressure = overburden_gradient * tvd
        
        # Calculate fracture pressure
        frac_pressure = (
            (poisson_ratio / (1 - poisson_ratio)) *
            (ob_pressure - pp_psi) + pp_psi
        )
        
        return Pressure(frac_pressure, "psi")

class WeightCalculator:
    """Utility class for weight calculations."""
    
    @staticmethod
    def buoyed_string_weight(
        true_weight: Weight,
        mud_weight: MudWeight,
        displacement: Volume
    ) -> Weight:
        """Calculate buoyed weight of drill string."""
        weight_lb = true_weight.to_unit("lbf")
        mud_ppg = mud_weight.to_unit("ppg")
        vol_bbl = displacement.to_unit("bbl")
        
        buoyancy_factor = 1 - (mud_ppg / 65.5)  # 65.5 ppg is steel density
        buoyed_weight = weight_lb * buoyancy_factor
        
        return Weight(buoyed_weight, "lbf")
    
    @staticmethod
    def hook_load(
        string_weight: Weight,
        friction_factor: float = 0.2
    ) -> Weight:
        """Calculate hook load considering friction."""
        weight_lb = string_weight.to_unit("lbf")
        
        # Add friction effect
        hook_load = weight_lb * (1 + friction_factor)
        return Weight(hook_load, "lbf")

class TorqueCalculator:
    """Utility class for torque calculations."""
    
    @staticmethod
    def drill_string_torque(
        weight_on_bit: Weight,
        friction_factor: float,
        hole_size: Diameter
    ) -> Torque:
        """Calculate drill string torque."""
        wob_lb = weight_on_bit.to_unit("lbf")
        hole_dia_in = hole_size.to_unit("in")
        
        torque = (wob_lb * friction_factor * hole_dia_in) / 24
        return Torque(torque, "ftlb")
    
    @staticmethod
    def motor_torque(
        differential_pressure: Pressure,
        displacement: float  # motor displacement in rev/gal
    ) -> Torque:
        """Calculate motor output torque."""
        diff_psi = differential_pressure.to_unit("psi")
        
        # Typical motor efficiency factor of 0.85
        torque = (diff_psi * displacement * 0.85) / (2 * math.pi)
        return Torque(torque, "ftlb")

class HydraulicsPower:
    """Utility class for hydraulics power calculations."""
    
    @staticmethod
    def calculate_hhp(
        pressure: Pressure,
        flow_rate: FlowRate
    ) -> float:
        """Calculate Hydraulic Horsepower."""
        p_psi = pressure.to_unit("psi")
        q_gpm = flow_rate.to_unit("gpm")
        
        return (p_psi * q_gpm) / 1714
    
    @staticmethod
    def jet_impact_force(
        flow_rate: FlowRate,
        fluid_density: Density,
        total_jet_area: Area
    ) -> Force:
        """Calculate jet impact force."""
        q_ft3s = flow_rate.to_unit("ft3/min") / 60
        rho_ppg = fluid_density.to_unit("ppg")
        a_in2 = total_jet_area.to_unit("in2")
        
        # Convert density to lb/ft³
        rho_lbft3 = rho_ppg * 8.33
        
        # Calculate velocity in ft/s
        velocity = (q_ft3s * 144) / a_in2
        
        # Calculate force in lbf
        force = (rho_lbft3 * q_ft3s * velocity) / 32.2
        return Force(force, "lbf")

def format_quantity(quantity: PhysicalQuantity, precision: int = 2) -> str:
    """Format a physical quantity for display."""
    return f"{quantity.value:.{precision}f} {quantity.unit}"

def parse_quantity(value: str, quantity_class: Type[PhysicalQuantity]) -> PhysicalQuantity:
    """Parse a string representation of a physical quantity."""
    try:
        numeric_value, unit = value.split()
        return quantity_class(float(numeric_value), unit)
    except ValueError:
        raise ValueError(f"Invalid format for {quantity_class.__name__}. Expected 'value unit'")

def convert_all_to_standard(quantities: Dict[str, PhysicalQuantity]) -> Dict[str, float]:
    """Convert all quantities to their standard units."""
    return {
        name: qty.to_unit(qty._default_unit)
        for name, qty in quantities.items()
    }

# Example usage:
"""
# Calculate ECD
mud_weight = MudWeight(12.5, "ppg")
annular_pressure = Pressure(500, "psi")
tvd = Depth(10000, "ft")
ecd = HydraulicsCalculator.calculate_ecd(mud_weight, annular_pressure, tvd)
print(f"ECD: {format_quantity(ecd)}")

# Calculate annular velocity
flow_rate = FlowRate(500, "gpm")
hole_size = Diameter(8.5, "in")
pipe_size = Diameter(5.0, "in")
velocity = HydraulicsCalculator.calculate_annular_velocity(flow_rate, hole_size, pipe_size)
print(f"Annular Velocity: {format_quantity(velocity)}")

# Calculate bottoms up time
depth = Depth(12000, "ft")
time = VolumeCalculator.calculate_bottoms_up_time(hole_size, pipe_size, depth, flow_rate)
print(f"Bottoms Up Time: {time:.1f} minutes")

# Calculate hydrostatic pressure
pressure = PressureCalculator.hydrostatic_pressure(mud_weight, depth)
print(f"Hydrostatic Pressure: {format_quantity(pressure)}")
"""
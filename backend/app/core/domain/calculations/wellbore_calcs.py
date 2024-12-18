# core/domain/calculations/wellbore_calcs.py

from typing import List, Tuple, Optional
from math import cos, log10, sin, radians, sqrt, pi
from dataclasses import dataclass
from ...units.quantity import (
    Length, Angle, Pressure, Temperature, Weight, Density, 
    Depth, Area, Volume, LinearDensity
)

class MinimumCurvatureCalculator:
    """
    Calculates wellbore trajectory using minimum curvature method
    """
    def __init__(self):
        self.epsilon = 1e-7  # Small number to handle zero dogleg cases

    def calculate_dogleg(self, inc1: Angle, azi1: Angle, 
                        inc2: Angle, azi2: Angle) -> Angle:
        """
        Calculate dogleg angle between two survey stations
        """
        # Convert to radians for calculation
        i1 = inc1.to_unit("rad")
        a1 = azi1.to_unit("rad")
        i2 = inc2.to_unit("rad")
        a2 = azi2.to_unit("rad")
        
        # Calculate dogleg using spherical trig formula
        cos_dog = cos(i1) * cos(i2) + sin(i1) * sin(i2) * cos(a2 - a1)
        
        # Handle numerical precision issues
        if cos_dog > 1:
            cos_dog = 1
        elif cos_dog < -1:
            cos_dog = -1
            
        dogleg_rad = abs(cos_dog)
        return Angle(dogleg_rad, "rad")

    def calculate_rf(self, dogleg: Angle) -> float:
        """
        Calculate ratio factor for minimum curvature method
        """
        dogleg_rad = dogleg.to_unit("rad")
        if abs(dogleg_rad) < self.epsilon:
            return 1.0
        return 2 * sin(dogleg_rad / 2) / dogleg_rad

    def calculate_position(self, 
                         md1: Depth, inc1: Angle, azi1: Angle,
                         md2: Depth, inc2: Angle, azi2: Angle) -> Tuple[Length, Length, Depth]:
        """
        Calculate position change between two survey stations using minimum curvature
        
        Returns:
        - northing change
        - easting change
        - tvd change
        """
        # Get step length
        dmd = md2.to_unit("ft") - md1.to_unit("ft")
        
        # Convert angles to radians
        i1 = inc1.to_unit("rad")
        a1 = azi1.to_unit("rad")
        i2 = inc2.to_unit("rad")
        a2 = azi2.to_unit("rad")
        
        # Calculate dogleg and ratio factor
        dogleg = self.calculate_dogleg(inc1, azi1, inc2, azi2)
        rf = self.calculate_rf(dogleg)
        
        # Calculate direction cosines
        north1 = sin(i1) * cos(a1)
        east1 = sin(i1) * sin(a1)
        tvd1 = cos(i1)
        
        north2 = sin(i2) * cos(a2)
        east2 = sin(i2) * sin(a2)
        tvd2 = cos(i2)
        
        # Calculate position changes
        dnorth = (dmd / 2) * (north1 + north2) * rf
        deast = (dmd / 2) * (east1 + east2) * rf
        dtvd = (dmd / 2) * (tvd1 + tvd2) * rf
        
        return (
            Length(dnorth, "ft"),
            Length(deast, "ft"), 
            Depth(dtvd, "ft")
        )

class TortuosityCalculator:
    """
    Calculates wellbore tortuosity and related parameters
    """
    def calculate_dls(self, dogleg: Angle, course_length: Length) -> Angle:
        """Calculate dogleg severity per 100 ft"""
        dogleg_deg = dogleg.to_unit("deg")
        length_ft = course_length.to_unit("ft")
        dls = (dogleg_deg * 100) / length_ft
        return Angle(dls, "deg/100ft")

    def calculate_build_rate(self, inc1: Angle, inc2: Angle, 
                           course_length: Length) -> Angle:
        """Calculate inclination build rate per 100 ft"""
        inc_change = inc2.to_unit("deg") - inc1.to_unit("deg")
        length_ft = course_length.to_unit("ft")
        build_rate = (inc_change * 100) / length_ft
        return Angle(build_rate, "deg/100ft")

    def calculate_turn_rate(self, azi1: Angle, azi2: Angle,
                          course_length: Length) -> Angle:
        """Calculate azimuth turn rate per 100 ft"""
        azi_change = azi2.to_unit("deg") - azi1.to_unit("deg")
        # Normalize azimuth change to -180 to 180
        if azi_change > 180:
            azi_change -= 360
        elif azi_change < -180:
            azi_change += 360
        
        length_ft = course_length.to_unit("ft")
        turn_rate = (azi_change * 100) / length_ft
        return Angle(turn_rate, "deg/100ft")

class WellboreGeometryCalculator:
    """
    Calculates wellbore geometric properties and volumes
    """
    def calculate_annular_capacity(self, 
                                 outer_diameter: Length,
                                 inner_diameter: Length) -> float:
        """
        Calculate annular capacity factor in bbl/ft
        """
        od_in = outer_diameter.to_unit("in")
        id_in = inner_diameter.to_unit("in")
        capacity = (od_in**2 - id_in**2) / 1029.4  # 1029.4 conversion factor to bbl/ft
        return capacity

    def calculate_volume(self, 
                        diameter: Length,
                        length: Length) -> Volume:
        """
        Calculate volume of a wellbore section
        """
        radius_ft = (diameter.to_unit("ft")) / 2
        length_ft = length.to_unit("ft")
        volume_cuft = pi * (radius_ft ** 2) * length_ft
        return Volume(volume_cuft, "ft3")

    def calculate_displacement(self, 
                             outer_diameter: Length,
                             inner_diameter: Length,
                             length: Length,
                             material_density: Density) -> Weight:
        """
        Calculate weight of material in annular space
        """
        od_ft = outer_diameter.to_unit("ft")
        id_ft = inner_diameter.to_unit("ft")
        length_ft = length.to_unit("ft")
        density_ppg = material_density.to_unit("lb/gal")
        
        volume_bbl = ((od_ft**2 - id_ft**2) * length_ft * 5.615) / 4
        weight_lbs = volume_bbl * density_ppg * 8.33  # 8.33 ppg = fresh water
        return Weight(weight_lbs, "lbf")

class PressureCalculator:
    """
    Calculates various pressure-related parameters
    """
    def calculate_hydrostatic_pressure(self, 
                                     tvd: Depth,
                                     fluid_density: Density) -> Pressure:
        """
        Calculate hydrostatic pressure at given TVD
        """
        tvd_ft = tvd.to_unit("ft")
        density_ppg = fluid_density.to_unit("lb/gal")
        pressure_psi = tvd_ft * density_ppg * 0.052  # 0.052 psi/ft/ppg conversion
        return Pressure(pressure_psi, "psi")

    def calculate_friction_pressure(self,
                                  flow_rate: float,
                                  fluid_density: Density,
                                  fluid_viscosity: float,
                                  pipe_diameter: Length,
                                  length: Length,
                                  roughness: float = 0.0001) -> Pressure:
        """
        Calculate friction pressure loss using Fanning friction factor
        """
        # Convert units
        d_ft = pipe_diameter.to_unit("ft")
        l_ft = length.to_unit("ft")
        density_ppg = fluid_density.to_unit("lb/gal")
        
        # Calculate Reynolds number
        velocity = flow_rate / (2.448 * (d_ft**2))  # ft/s
        re = (928 * density_ppg * velocity * d_ft) / fluid_viscosity
        
        # Calculate friction factor (Colebrook correlation)
        f = 0.02  # Initial guess
        for _ in range(20):  # Iterate to converge
            f_new = (-2 * log10(roughness/(3.7*d_ft) + 2.51/(re*sqrt(f))))**(-2)
            if abs(f - f_new) < 0.0001:
                break
            f = f_new
        
        # Calculate pressure loss
        pressure_psi = (f * density_ppg * velocity**2 * l_ft) / (25.8 * d_ft)
        return Pressure(pressure_psi, "psi")

class TemperatureCalculator:
    """
    Calculates temperature profiles and effects
    """
    def calculate_temp_at_depth(self,
                              surface_temp: Temperature,
                              gradient: float,
                              depth: Depth) -> Temperature:
        """
        Calculate temperature at depth given surface temperature and gradient
        """
        surface_f = surface_temp.to_unit("degF")
        depth_ft = depth.to_unit("ft")
        temp_f = surface_f + (gradient * depth_ft)
        return Temperature(temp_f, "degF")

    def calculate_thermal_expansion(self,
                                 initial_length: Length,
                                 temp_change: Temperature,
                                 thermal_coeff: float) -> Length:
        """
        Calculate thermal expansion of tubular
        """
        length_ft = initial_length.to_unit("ft")
        delta_t = temp_change.to_unit("degF")
        expansion = length_ft * (1 + thermal_coeff * delta_t)
        return Length(expansion, "ft")

class ECD_Calculator:
    """
    Calculates Equivalent Circulating Density
    """
    def calculate_ecd(self,
                     static_density: Density,
                     annular_pressure_loss: Pressure,
                     true_vertical_depth: Depth) -> Density:
        """
        Calculate Equivalent Circulating Density
        """
        mud_weight_ppg = static_density.to_unit("lb/gal")
        apl_psi = annular_pressure_loss.to_unit("psi")
        tvd_ft = true_vertical_depth.to_unit("ft")
        
        ecd_ppg = mud_weight_ppg + (apl_psi / (0.052 * tvd_ft))
        return Density(ecd_ppg, "lb/gal")

class LoadCalculator:
    """
    Calculates various loads on wellbore tubulars
    """
    def calculate_buoyed_weight(self,
                              pipe_weight: LinearDensity,
                              fluid_density: Density) -> LinearDensity:
        """
        Calculate buoyed weight of pipe
        """
        weight_ppf = pipe_weight.to_unit("lb/ft")
        mud_weight_ppg = fluid_density.to_unit("lb/gal")
        
        buoyancy_factor = 1 - (mud_weight_ppg / 65.5)  # 65.5 ppg is steel density
        buoyed_weight = weight_ppf * buoyancy_factor
        
        return LinearDensity(buoyed_weight, "lb/ft")

    def calculate_hook_load(self,
                          pipe_segments: List[Tuple[LinearDensity, Length]],
                          fluid_density: Density,
                          friction_factor: float = 0.3) -> Weight:
        """
        Calculate hook load considering pipe weight and friction
        """
        total_load = 0
        
        for weight_per_ft, length in pipe_segments:
            # Convert units
            ppf = weight_per_ft.to_unit("lb/ft")
            len_ft = length.to_unit("ft")
            
            # Calculate segment weight
            segment_weight = ppf * len_ft
            
            # Apply buoyancy
            mud_weight_ppg = fluid_density.to_unit("lb/gal")
            buoyancy_factor = 1 - (mud_weight_ppg / 65.5)
            buoyed_weight = segment_weight * buoyancy_factor
            
            # Apply friction factor
            total_load += buoyed_weight * (1 + friction_factor)
        
        return Weight(total_load, "lbf")

def calculate_critical_buckling_force(
        pipe_properties: dict,
        hole_size: Length,
        inclination: Angle,
        fluid_density: Density) -> Weight:
    """
    Calculate critical buckling force
    """
    # Extract pipe properties
    E = pipe_properties["youngs_modulus"]  # psi
    I = pipe_properties["moment_of_inertia"]  # in^4
    
    # Convert units
    hole_diameter = hole_size.to_unit("in")
    inc_rad = inclination.to_unit("rad")
    density_ppg = fluid_density.to_unit("lb/gal")
    
    # Calculate weight per foot of pipe material
    buoyed_weight_per_foot = (pipe_properties["weight_per_foot"] * 
                             (1 - density_ppg/65.5))
    
    # Calculate critical force
    Fc = 2 * sqrt((E * I * buoyed_weight_per_foot * cos(inc_rad)) / 
                  (hole_diameter - pipe_properties["outer_diameter"]))
    
    return Weight(Fc, "lbf")

class WellborePressureIntegrityCalculator:
    """
    Calculates wellbore pressure integrity and related parameters
    """
    
    def calculate_fracture_pressure(self,
                                  depth: Depth,
                                  pore_pressure: Pressure,
                                  poisson_ratio: float,
                                  min_horizontal_stress_gradient: float) -> Pressure:
        """
        Calculate fracture pressure using minimum horizontal stress method
        """
        depth_ft = depth.to_unit("ft")
        pore_psi = pore_pressure.to_unit("psi")
        
        # Calculate minimum horizontal stress
        min_stress = min_horizontal_stress_gradient * depth_ft
        
        # Calculate fracture pressure
        frac_pressure = (min_stress + pore_psi * (poisson_ratio / (1 - poisson_ratio)))
        
        return Pressure(frac_pressure, "psi")
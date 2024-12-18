# app/core/units/quantity.py
from typing import Dict, List, Tuple, Union, Optional, Any
from pydantic import BaseModel, validator
from decimal import Decimal
import math

class PhysicalQuantity:
    """Base class for all physical quantities."""
    
    # Class-level unit conversion mappings
    _units: Dict[str, float] = {}
    _default_unit: str = ""
    _valid_units: set = set()
    
    def __init__(self, value: Union[float, int, Decimal], unit: str):
        """
        Initialize a physical quantity.
        
        Args:
            value: The numerical value
            unit: The unit of measurement
        """
        self.value = float(value)
        if unit not in self._valid_units:
            raise ValueError(f"Invalid unit: {unit}. Valid units are: {self._valid_units}")
        self.unit = unit

    def to_unit(self, target_unit: str) -> float:
        """Convert the value to a different unit."""
        if target_unit not in self._valid_units:
            raise ValueError(f"Invalid target unit: {target_unit}")
            
        if self.unit == target_unit:
            return self.value
            
        # Convert to base unit first
        base_value = self.value * self._units[self.unit]
        # Then convert to target unit
        return base_value / self._units[target_unit]

    def convert_to(self, target_unit: str) -> 'PhysicalQuantity':
        """Return a new quantity in the target unit."""
        return self.__class__(self.to_unit(target_unit), target_unit)

    def __add__(self, other: 'PhysicalQuantity') -> 'PhysicalQuantity':
        """Add two quantities of the same type."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot add {type(self)} and {type(other)}")
        result_value = self.value + other.to_unit(self.unit)
        return self.__class__(result_value, self.unit)

    def __sub__(self, other: 'PhysicalQuantity') -> 'PhysicalQuantity':
        """Subtract two quantities of the same type."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot subtract {type(self)} and {type(other)}")
        result_value = self.value - other.to_unit(self.unit)
        return self.__class__(result_value, self.unit)

    def __mul__(self, other: Union[int, float]) -> 'PhysicalQuantity':
        """Multiply quantity by a scalar."""
        return self.__class__(self.value * other, self.unit)

    def __truediv__(self, other: Union[int, float, 'PhysicalQuantity']) -> Union['PhysicalQuantity', float]:
        """Divide quantity by a scalar or another quantity."""
        if isinstance(other, (int, float)):
            return self.__class__(self.value / other, self.unit)
        if isinstance(other, PhysicalQuantity):
            # If same type, return dimensionless ratio
            if isinstance(other, self.__class__):
                return self.value / other.to_unit(self.unit)
            raise TypeError(f"Cannot divide {type(self)} by {type(other)}")

    def __eq__(self, other: 'PhysicalQuantity') -> bool:
        """Compare two quantities for equality."""
        if not isinstance(other, self.__class__):
            return False
        return math.isclose(self.to_unit(self._default_unit), 
                          other.to_unit(self._default_unit),
                          rel_tol=1e-9)

    def __lt__(self, other: 'PhysicalQuantity') -> bool:
        """Compare if this quantity is less than another."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot compare {type(self)} and {type(other)}")
        return self.to_unit(self._default_unit) < other.to_unit(self._default_unit)

    def __repr__(self) -> str:
        """String representation of the quantity."""
        return f"{self.__class__.__name__}({self.value}, '{self.unit}')"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.value} {self.unit}"

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "value": self.value,
            "unit": self.unit
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PhysicalQuantity':
        """Create instance from dictionary."""
        return cls(data["value"], data["unit"])

    def round(self, decimals: int = 2) -> 'PhysicalQuantity':
        """Round the value to specified decimal places."""
        return self.__class__(round(self.value, decimals), self.unit)

    @classmethod
    def get_valid_units(cls) -> set:
        """Get the set of valid units for this quantity."""
        return cls._valid_units

    @classmethod
    def validate_unit(cls, unit: str) -> bool:
        """Check if a unit is valid for this quantity."""
        return unit in cls._valid_units

class Length(PhysicalQuantity):
    """Length quantity with common oil field units."""
    
    # Define units relative to meters (SI base unit)
    _units = {
        "m": 1.0,           # meter (base unit)
        "ft": 0.3048,       # feet
        "in": 0.0254,       # inches
        "mm": 0.001,        # millimeters
        "cm": 0.01,         # centimeters
        "yd": 0.9144,       # yards
    }
    _default_unit = "ft"    # Common in oil field
    _valid_units = set(_units.keys())

    def to_meters(self) -> float:
        """Convert to meters."""
        return self.to_unit("m")

    def to_feet(self) -> float:
        """Convert to feet."""
        return self.to_unit("ft")

class Depth(Length):
    """Specialized length class for well depths.
    
    While technically the same as Length, this class exists to:
    1. Make the code more semantically clear
    2. Allow for potential depth-specific operations
    3. Enable type checking to catch logical errors
    """
    
    def __init__(self, value: Union[float, int, Decimal], unit: str = "ft"):
        """Initialize depth, defaulting to feet."""
        super().__init__(value, unit)
        
    def from_kb(self) -> bool:
        """Whether depth is measured from kelly bushing."""
        # For future implementation
        return True
        
    def to_tvd(self) -> 'Depth':
        """Convert measured depth to true vertical depth."""
        # For future implementation
        return self
        
    def to_md(self) -> 'Depth':
        """Convert true vertical depth to measured depth."""
        # For future implementation
        return self

    def calculate_hydrostatic_pressure(self, mud_weight: 'Density') -> 'Pressure':
        """Calculate hydrostatic pressure at this depth."""
      
        # Convert depth to feet and mud weight to ppg for calculation
        depth_ft = self.to_feet()
        mud_ppg = mud_weight.to_ppg()
        
        # Hydrostatic pressure (psi) = 0.052 * depth (ft) * mud weight (ppg)
        pressure_psi = 0.052 * depth_ft * mud_ppg
        return Pressure(pressure_psi, "psi")
    
    # app/core/units/quantity.py (continued)

class Weight(PhysicalQuantity):
    """Weight (force) measurements for oil field operations."""
    
    _units = {
        "N": 1.0,           # Newtons (SI base unit)
        "lbf": 4.44822,     # pounds force
        "kgf": 9.80665,     # kilograms force
        "klbf": 4448.22,    # kilo-pounds force
        "ton": 8896.44,     # short tons (2000 lbf)
        "tonne": 9806.65,   # metric tonnes
    }
    _default_unit = "lbf"   # Common in oil field
    _valid_units = set(_units.keys())
    
    def to_klbf(self) -> float:
        """Convert to kilo-pounds force (common in heavy lift operations)."""
        return self.to_unit("klbf")

class MudWeight(PhysicalQuantity):
    """Specialized class for drilling fluid density."""
    
    _units = {
        "ppg": 1.0,         # pounds per gallon (US oilfield standard)
        "sg": 8.345,        # specific gravity
        "kg/m3": 119.826,   # kilograms per cubic meter
        "kg/L": 8.345,      # kilograms per liter
        "lb/ft3": 7.48052,  # pounds per cubic foot
        "psi/1000ft": 52.0  # pressure gradient per 1000ft
    }
    _default_unit = "ppg"
    _valid_units = set(_units.keys())
    
    # def get_hydrostatic_pressure(self, tvd: Length) -> Pressure:
    #     """Calculate hydrostatic pressure at given TVD."""
    #     mud_ppg = self.to_unit("ppg")
    #     depth_ft = tvd.to_unit("ft")
    #     pressure_psi = mud_ppg * 0.052 * depth_ft
    #     return FluidPressure(pressure_psi, "psi")
    
    def check_barite_sag_risk(self) -> str:
        """Evaluate risk of barite sag based on mud weight."""
        ppg = self.to_unit("ppg")
        if ppg < 12.0:
            return "Low Risk"
        elif ppg < 16.0:
            return "Moderate Risk"
        else:
            return "High Risk - Consider sag mitigation measures"
    
    @classmethod
    def from_pressure_gradient(cls, gradient: float, unit: str = "psi/ft") -> 'MudWeight':
        """Create mud weight from pressure gradient."""
        if unit == "psi/ft":
            ppg = gradient / 0.052
            return cls(ppg, "ppg")
        raise ValueError(f"Unsupported gradient unit: {unit}")

class Pressure(PhysicalQuantity):
    """Enhanced pressure measurements for drilling operations."""
    
    _units = {
        "psi": 1.0,         # pounds per square inch (base unit for oilfield)
        "kPa": 6.89476,     # kilopascals
        "MPa": 6894.76,     # megapascals
        "bar": 68.9476,     # bars
        "kg/cm2": 70.307,   # kilograms per square centimeter
        "ppg": 0.052,       # pounds per gallon (as gradient)
        "psi/ft": 1.0       # pressure gradient
    }
    _default_unit = "psi"
    _valid_units = set(_units.keys())
    
    def get_gradient(self, depth: Length) -> float:
        """Calculate pressure gradient in psi/ft."""
        return self.to_unit("psi") / depth.to_unit("ft")
    
    def to_mud_weight(self) -> MudWeight:
        """Convert pressure gradient to mud weight."""
        psi_ft = self.to_unit("psi/ft")
        ppg = psi_ft / 0.052
        return MudWeight(ppg, "ppg")
    
    def check_fracture_pressure(self, frac_pressure: 'Pressure', 
                              safety_margin: float = 0.5) -> bool:
        """Check if pressure is safely below fracture pressure."""
        return self.to_unit("psi") <= (frac_pressure.to_unit("psi") * 
                                     (1 - safety_margin))

class Density(PhysicalQuantity):
    """Enhanced density measurements for drilling fluids and materials."""
    
    _units = {
        "kg/m3": 1.0,          # kilograms per cubic meter (SI)
        "ppg": 119.826427,     # pounds per gallon (US oilfield)
        "lb/ft3": 16.0185,     # pounds per cubic foot
        "g/cm3": 1000.0,       # grams per cubic centimeter
        "sg": 1000.0,          # specific gravity (relative to water)
        "psi/ft": 0.052,       # pressure gradient
        "kg/L": 1000.0,        # kilograms per liter
        "lb/bbl": 2.853,       # pounds per barrel
    }
    _default_unit = "ppg"      # Common in oil field
    _valid_units = set(_units.keys())
    
    def to_pressure_gradient(self) -> float:
        """Convert density to pressure gradient in psi/ft."""
        ppg = self.to_unit("ppg")
        return ppg * 0.052
    
    def calculate_hydrostatic_pressure(self, depth: Length) -> Pressure:
        """Calculate hydrostatic pressure at given depth."""
        gradient = self.to_pressure_gradient()
        depth_ft = depth.to_unit("ft")
        return Pressure(gradient * depth_ft, "psi")
    
    def get_equivalent_mud_weight(self) -> MudWeight:
        """Convert to equivalent mud weight."""
        ppg = self.to_unit("ppg")
        return MudWeight(ppg, "ppg")
    
    def check_barite_sag_risk(self) -> str:
        """Evaluate risk of barite sag."""
        ppg = self.to_unit("ppg")
        if ppg < 12.0:
            return "Low Risk"
        elif ppg < 16.0:
            return "Moderate Risk - Monitor"
        else:
            return "High Risk - Implement sag mitigation"
    
    def calculate_equivalent_density(self, additional_pressure: Pressure, 
                                   depth: Length) -> 'Density':
        """Calculate equivalent density including additional pressure."""
        base_pressure = self.calculate_hydrostatic_pressure(depth)
        total_pressure = base_pressure.to_unit("psi") + additional_pressure.to_unit("psi")
        equiv_ppg = (total_pressure / depth.to_unit("ft")) / 0.052
        return Density(equiv_ppg, "ppg")

class Diameter(Length):
    """Specialized length class for diameters.
    
    While technically the same as Length, this class:
    1. Makes the code more semantically clear
    2. Defaults to inches (common in oil field)
    3. Adds diameter-specific calculations
    """
    
    _default_unit = "in"  # Oil field typically uses inches for diameters
    
    def __init__(self, value: Union[float, int, Decimal], unit: str = "in"):
        """Initialize diameter, defaulting to inches."""
        super().__init__(value, unit)
    
    def get_area(self) -> 'Area':
        """Calculate circular area from diameter."""
        radius = self.value / 2
        area_sq_units = math.pi * (radius ** 2)
        
        # Return area in square units corresponding to diameter units
        if self.unit == "in":
            return Area(area_sq_units, "in2")
        elif self.unit == "ft":
            return Area(area_sq_units, "ft2")
        elif self.unit == "m":
            return Area(area_sq_units, "m2")
        else:
            # Convert to inches first, then calculate
            return self.convert_to("in").get_area()

    def get_circumference(self) -> Length:
        """Calculate circumference."""
        return Length(math.pi * self.value, self.unit)

class Azimuth(PhysicalQuantity):
    """Angular measurement class for wellbore direction."""
    
    _units = {
        "deg": 1.0,         # degrees
        "rad": 57.2958,     # radians (converted to degrees)
        "grad": 0.9,        # gradians
    }
    _default_unit = "deg"
    _valid_units = set(_units.keys())
    
    def __init__(self, value: Union[float, int, Decimal], unit: str = "deg"):
        """Initialize azimuth, normalizing to 0-360 degrees."""
        super().__init__(value, unit)
        if unit == "deg":
            self.value = self.value % 360
    
    def to_bearing(self) -> str:
        """Convert azimuth to bearing (N/S E/W) format."""
        deg = self.to_unit("deg")
        if deg == 0 or deg == 360:
            return "N"
        elif deg == 90:
            return "E"
        elif deg == 180:
            return "S"
        elif deg == 270:
            return "W"
        
        # Calculate quadrant
        if 0 < deg < 90:
            return f"N {deg}° E"
        elif 90 < deg < 180:
            return f"S {180 - deg}° E"
        elif 180 < deg < 270:
            return f"S {deg - 180}° W"
        else:
            return f"N {360 - deg}° W"

class Area(PhysicalQuantity):
    """Area measurements common in oil field operations."""
    
    _units = {
        "m2": 1.0,          # square meters (SI base unit)
        "ft2": 0.092903,    # square feet
        "in2": 0.00064516,  # square inches
        "ac": 4046.86,      # acres
        "ha": 10000.0,      # hectares
    }
    _default_unit = "ft2"   # Common in oil field
    _valid_units = set(_units.keys())

class Weight(PhysicalQuantity):
    """Weight (force) measurements for oil field operations."""
    
    _units = {
        "N": 1.0,           # Newtons (SI base unit)
        "lbf": 4.44822,     # pounds force
        "kgf": 9.80665,     # kilograms force
        "klbf": 4448.22,    # kilo-pounds force
        "ton": 8896.44,     # short tons (2000 lbf)
        "tonne": 9806.65,   # metric tonnes
    }
    _default_unit = "lbf"   # Common in oil field
    _valid_units = set(_units.keys())
    
    def to_klbf(self) -> float:
        """Convert to kilo-pounds force (common in heavy lift operations)."""
        return self.to_unit("klbf")

class LinearDensity(PhysicalQuantity):
    """Weight per unit length, common for pipe specifications."""
    
    _units = {
        "kg/m": 1.0,        # kilograms per meter (SI base unit)
        "lb/ft": 1.48816,   # pounds per foot
        "lb/in": 17.8579,   # pounds per inch
    }
    _default_unit = "lb/ft" # Common in oil field
    _valid_units = set(_units.keys())
    
    def get_weight(self, length: Length) -> Weight:
        """Calculate total weight for a given length."""
        # Convert everything to consistent units (lb/ft and ft)
        density_lb_ft = self.to_unit("lb/ft")
        length_ft = length.to_unit("ft")
        
        return Weight(density_lb_ft * length_ft, "lbf")

class Torque(PhysicalQuantity):
    """Torque measurements for oil field operations."""
    
    _units = {
        "Nm": 1.0,          # Newton-meters (SI base unit)
        "ftlb": 1.35582,    # foot-pounds
        "kftlb": 1355.82,   # kilo foot-pounds
        "inlb": 0.112985,   # inch-pounds
    }
    _default_unit = "ftlb"  # Common in oil field
    _valid_units = set(_units.keys())
    
    def to_kftlb(self) -> float:
        """Convert to kilo foot-pounds (common in drilling operations)."""
        return self.to_unit("kftlb")

class BarrelOfOilEquivalent(PhysicalQuantity):
    """Barrel of oil equivalent (BOE) for hydrocarbon volume normalization."""
    
    _units = {
        "boe": 1.0,         # barrel of oil equivalent (base unit)
        "mcf": 0.1667,      # thousand cubic feet (assuming 6 mcf = 1 boe)
        "mmbtu": 0.172414,  # million British thermal units
        "GJ": 0.163401,     # gigajoules
    }
    _default_unit = "boe"
    _valid_units = set(_units.keys())
    
    @classmethod
    def from_gas_volume(cls, gas_volume: float, heating_value: float = 1000) -> 'BarrelOfOilEquivalent':
        """Convert natural gas volume to BOE based on heating value.
        
        Args:
            gas_volume: Volume in MCF
            heating_value: BTU per cubic foot (default 1000 for standard natural gas)
        """
        boe = (gas_volume * heating_value) / (5.8 * 10**6)  # 5.8 MMBtu per BOE
        return cls(boe, "boe")

class DLS(PhysicalQuantity):
    """Dog Leg Severity - rate of change of wellbore direction."""
    
    _units = {
        "deg/100ft": 1.0,       # degrees per 100 feet (common US)
        "deg/30m": 0.9144,      # degrees per 30 meters
        "rad/30m": 0.0159,      # radians per 30 meters
    }
    _default_unit = "deg/100ft"
    _valid_units = set(_units.keys())
    
    def is_excessive(self, tool_limit: float = 3.0) -> bool:
        """Check if DLS exceeds typical tool limitations."""
        return self.to_unit("deg/100ft") > tool_limit
    
    def calculate_minimum_radius(self) -> Length:
        """Calculate minimum radius of curvature."""
        dls_deg_per_100ft = self.to_unit("deg/100ft")
        radius_ft = 100 / (2 * math.sin(math.radians(dls_deg_per_100ft / 2)))
        return Length(radius_ft, "ft")

class FluidDensity(Density):
    """Specialized density class for drilling and completion fluids."""
    
    _units = {
        "kg/m3": 1.0,          # kilogram per cubic meter (SI base unit)
        "ppg": 119.826427,     # pounds per gallon (common US oilfield)
        "lb/ft3": 16.0185,     # pounds per cubic foot
        "sg": 1000.0,          # specific gravity (relative to water)
        "psi/ft": 19.25,       # pressure gradient (freshwater ≈ 0.433 psi/ft)
    }
    _default_unit = "ppg"
    _valid_units = set(_units.keys())
    
    def get_pressure_gradient(self) -> float:
        """Calculate pressure gradient in psi/ft."""
        ppg = self.to_unit("ppg")
        return ppg * 0.052  # Standard oilfield conversion
    
    def get_hydrostatic_pressure(self, depth: Length) -> 'FluidPressure':
        """Calculate hydrostatic pressure at given depth."""
        gradient = self.get_pressure_gradient()
        pressure = gradient * depth.to_unit("ft")
        return FluidPressure(pressure, "psi")
    
    def ecd_from_annular_pressure(self, depth: Length, annular_pressure: 'FluidPressure') -> 'FluidDensity':
        """Calculate Equivalent Circulating Density (ECD) from annular pressure."""
        pressure_gradient = annular_pressure.to_unit("psi") / depth.to_unit("ft")
        ecd_ppg = pressure_gradient / 0.052
        return FluidDensity(ecd_ppg, "ppg")

class Energy(PhysicalQuantity):
    """Energy measurements for oil and gas operations."""
    
    _units = {
        "J": 1.0,               # Joules (SI base unit)
        "kJ": 1000.0,          # kilojoules
        "BTU": 1055.06,        # British Thermal Units
        "mmBTU": 1.055e9,      # million BTU
        "kWh": 3.6e6,          # kilowatt hours
        "ftlb": 1.35582,       # foot pounds
    }
    _default_unit = "BTU"
    _valid_units = set(_units.keys())
    
    @classmethod
    def from_natural_gas(cls, volume: float, heating_value: float = 1000) -> 'Energy':
        """Calculate energy content of natural gas.
        
        Args:
            volume: Volume in MCF
            heating_value: BTU per cubic foot
        """
        btu = volume * 1000 * heating_value  # MCF to CF * BTU/CF
        return cls(btu, "BTU")

class FluidPressure(Pressure):
    """Specialized pressure class for fluid systems."""
    
    def __init__(self, value: Union[float, int, Decimal], unit: str = "psi"):
        super().__init__(value, unit)
    
    def to_mud_weight(self, depth: Length) -> FluidDensity:
        """Convert pressure to equivalent mud weight."""
        pressure_psi = self.to_unit("psi")
        depth_ft = depth.to_unit("ft")
        ppg = pressure_psi / (0.052 * depth_ft)
        return FluidDensity(ppg, "ppg")
    
    def is_overbalanced(self, pore_pressure: 'FluidPressure', margin: float = 200) -> bool:
        """Check if pressure provides adequate overbalance."""
        return self.to_unit("psi") > (pore_pressure.to_unit("psi") + margin)
    
    def calculate_fracture_gradient(self, depth: Length) -> float:
        """Calculate fracture gradient in psi/ft."""
        return self.to_unit("psi") / depth.to_unit("ft")

class FluidVolume(PhysicalQuantity):
    """Volume measurements for drilling and completion fluids."""
    
    _units = {
        "m3": 1.0,          # cubic meters (SI base unit)
        "bbl": 0.158987,    # barrels (oil field standard)
        "gal": 0.00378541,  # gallons
        "ft3": 0.0283168,   # cubic feet
        "L": 0.001,         # liters
    }
    _default_unit = "bbl"
    _valid_units = set(_units.keys())
    
    def calculate_displacement(self, length: Length, diameter: Diameter) -> 'FluidVolume':
        """Calculate volume displaced by pipe."""
        area = diameter.get_area()
        volume_ft3 = area.to_unit("ft2") * length.to_unit("ft")
        return FluidVolume(volume_ft3 * 5.615, "bbl")  # Convert ft3 to bbl
    
    def calculate_annular_capacity(self, hole_size: Diameter, pipe_size: Diameter) -> float:
        """Calculate annular capacity in bbl/ft."""
        hole_area = hole_size.get_area()
        pipe_area = pipe_size.get_area()
        annular_area_in2 = hole_area.to_unit("in2") - pipe_area.to_unit("in2")
        return (annular_area_in2 * 0.0006944)  # Convert in2 to bbl/ft

class Force(PhysicalQuantity):
    """Force measurements for mechanical calculations."""
    
    _units = {
        "N": 1.0,           # Newtons (SI base unit)
        "lbf": 4.44822,     # pounds force
        "kN": 1000.0,       # kilonewtons
        "klbf": 4448.22,    # kilo-pounds force
        "daN": 10.0,        # decanewtons (common in some equipment specs)
    }
    _default_unit = "lbf"
    _valid_units = set(_units.keys())
    
    def calculate_stress(self, area: Area) -> Pressure:
        """Calculate stress from force and area."""
        force_lbf = self.to_unit("lbf")
        area_in2 = area.to_unit("in2")
        return Pressure(force_lbf / area_in2, "psi")
    
    def calculate_hook_load(self, buoyed_weight: Weight, friction: float = 0.1) -> 'Force':
        """Calculate hook load considering friction.
        
        Args:
            buoyed_weight: Buoyed weight of string
            friction: Friction factor (default 0.1 for typical wellbore)
        """
        weight_lbf = buoyed_weight.to_unit("lbf")
        drag = weight_lbf * friction
        return Force(weight_lbf + drag, "lbf")
    
 # app/core/units/quantity.py (continued)

class BarrelOfOilEquivalent(PhysicalQuantity):
    """Barrel of oil equivalent (BOE) for hydrocarbon volume normalization."""
    
    _units = {
        "boe": 1.0,         # barrel of oil equivalent (base unit)
        "mcf": 0.1667,      # thousand cubic feet (assuming 6 mcf = 1 boe)
        "mmbtu": 0.172414,  # million British thermal units
        "GJ": 0.163401,     # gigajoules
    }
    _default_unit = "boe"
    _valid_units = set(_units.keys())
    
    @classmethod
    def from_gas_volume(cls, gas_volume: float, heating_value: float = 1000) -> 'BarrelOfOilEquivalent':
        """Convert natural gas volume to BOE based on heating value.
        
        Args:
            gas_volume: Volume in MCF
            heating_value: BTU per cubic foot (default 1000 for standard natural gas)
        """
        boe = (gas_volume * heating_value) / (5.8 * 10**6)  # 5.8 MMBtu per BOE
        return cls(boe, "boe")

class DLS(PhysicalQuantity):
    """Dog Leg Severity - rate of change of wellbore direction."""
    
    _units = {
        "deg/100ft": 1.0,       # degrees per 100 feet (common US)
        "deg/30m": 0.9144,      # degrees per 30 meters
        "rad/30m": 0.0159,      # radians per 30 meters
    }
    _default_unit = "deg/100ft"
    _valid_units = set(_units.keys())
    
    def is_excessive(self, tool_limit: float = 3.0) -> bool:
        """Check if DLS exceeds typical tool limitations."""
        return self.to_unit("deg/100ft") > tool_limit
    
    def calculate_minimum_radius(self) -> Length:
        """Calculate minimum radius of curvature."""
        dls_deg_per_100ft = self.to_unit("deg/100ft")
        radius_ft = 100 / (2 * math.sin(math.radians(dls_deg_per_100ft / 2)))
        return Length(radius_ft, "ft")

class FluidDensity(Density):
    """Specialized density class for drilling and completion fluids."""
    
    _units = {
        "kg/m3": 1.0,          # kilogram per cubic meter (SI base unit)
        "ppg": 119.826427,     # pounds per gallon (common US oilfield)
        "lb/ft3": 16.0185,     # pounds per cubic foot
        "sg": 1000.0,          # specific gravity (relative to water)
        "psi/ft": 19.25,       # pressure gradient (freshwater ≈ 0.433 psi/ft)
    }
    _default_unit = "ppg"
    _valid_units = set(_units.keys())
    
    def get_pressure_gradient(self) -> float:
        """Calculate pressure gradient in psi/ft."""
        ppg = self.to_unit("ppg")
        return ppg * 0.052  # Standard oilfield conversion
    
    def get_hydrostatic_pressure(self, depth: Length) -> 'FluidPressure':
        """Calculate hydrostatic pressure at given depth."""
        gradient = self.get_pressure_gradient()
        pressure = gradient * depth.to_unit("ft")
        return FluidPressure(pressure, "psi")
    
    def ecd_from_annular_pressure(self, depth: Length, annular_pressure: 'FluidPressure') -> 'FluidDensity':
        """Calculate Equivalent Circulating Density (ECD) from annular pressure."""
        pressure_gradient = annular_pressure.to_unit("psi") / depth.to_unit("ft")
        ecd_ppg = pressure_gradient / 0.052
        return FluidDensity(ecd_ppg, "ppg")

class Energy(PhysicalQuantity):
    """Energy measurements for oil and gas operations."""
    
    _units = {
        "J": 1.0,               # Joules (SI base unit)
        "kJ": 1000.0,          # kilojoules
        "BTU": 1055.06,        # British Thermal Units
        "mmBTU": 1.055e9,      # million BTU
        "kWh": 3.6e6,          # kilowatt hours
        "ftlb": 1.35582,       # foot pounds
    }
    _default_unit = "BTU"
    _valid_units = set(_units.keys())
    
    @classmethod
    def from_natural_gas(cls, volume: float, heating_value: float = 1000) -> 'Energy':
        """Calculate energy content of natural gas.
        
        Args:
            volume: Volume in MCF
            heating_value: BTU per cubic foot
        """
        btu = volume * 1000 * heating_value  # MCF to CF * BTU/CF
        return cls(btu, "BTU")

class FluidPressure(Pressure):
    """Specialized pressure class for fluid systems."""
    
    def __init__(self, value: Union[float, int, Decimal], unit: str = "psi"):
        super().__init__(value, unit)
    
    def to_mud_weight(self, depth: Length) -> FluidDensity:
        """Convert pressure to equivalent mud weight."""
        pressure_psi = self.to_unit("psi")
        depth_ft = depth.to_unit("ft")
        ppg = pressure_psi / (0.052 * depth_ft)
        return FluidDensity(ppg, "ppg")
    
    def is_overbalanced(self, pore_pressure: 'FluidPressure', margin: float = 200) -> bool:
        """Check if pressure provides adequate overbalance."""
        return self.to_unit("psi") > (pore_pressure.to_unit("psi") + margin)
    
    def calculate_fracture_gradient(self, depth: Length) -> float:
        """Calculate fracture gradient in psi/ft."""
        return self.to_unit("psi") / depth.to_unit("ft")

class FluidVolume(PhysicalQuantity):
    """Volume measurements for drilling and completion fluids."""
    
    _units = {
        "m3": 1.0,          # cubic meters (SI base unit)
        "bbl": 0.158987,    # barrels (oil field standard)
        "gal": 0.00378541,  # gallons
        "ft3": 0.0283168,   # cubic feet
        "L": 0.001,         # liters
    }
    _default_unit = "bbl"
    _valid_units = set(_units.keys())
    
    def calculate_displacement(self, length: Length, diameter: Diameter) -> 'FluidVolume':
        """Calculate volume displaced by pipe."""
        area = diameter.get_area()
        volume_ft3 = area.to_unit("ft2") * length.to_unit("ft")
        return FluidVolume(volume_ft3 * 5.615, "bbl")  # Convert ft3 to bbl
    
    def calculate_annular_capacity(self, hole_size: Diameter, pipe_size: Diameter) -> float:
        """Calculate annular capacity in bbl/ft."""
        hole_area = hole_size.get_area()
        pipe_area = pipe_size.get_area()
        annular_area_in2 = hole_area.to_unit("in2") - pipe_area.to_unit("in2")
        return (annular_area_in2 * 0.0006944)  # Convert in2 to bbl/ft

class Force(PhysicalQuantity):
    """Force measurements for mechanical calculations."""
    
    _units = {
        "N": 1.0,           # Newtons (SI base unit)
        "lbf": 4.44822,     # pounds force
        "kN": 1000.0,       # kilonewtons
        "klbf": 4448.22,    # kilo-pounds force
        "daN": 10.0,        # decanewtons (common in some equipment specs)
    }
    _default_unit = "lbf"
    _valid_units = set(_units.keys())
    
    def calculate_stress(self, area: Area) -> Pressure:
        """Calculate stress from force and area."""
        force_lbf = self.to_unit("lbf")
        area_in2 = area.to_unit("in2")
        return Pressure(force_lbf / area_in2, "psi")
    
    def calculate_hook_load(self, buoyed_weight: Weight, friction: float = 0.1) -> 'Force':
        """Calculate hook load considering friction.
        
        Args:
            buoyed_weight: Buoyed weight of string
            friction: Friction factor (default 0.1 for typical wellbore)
        """
        weight_lbf = buoyed_weight.to_unit("lbf")
        drag = weight_lbf * friction
        return Force(weight_lbf + drag, "lbf")  
    
 # app/core/units/quantity.py (continued)

class Mass(PhysicalQuantity):
    """Mass measurements for material calculations."""
    
    _units = {
        "kg": 1.0,          # kilograms (SI base unit)
        "lb": 0.453592,     # pounds mass
        "g": 0.001,         # grams
        "mt": 1000.0,       # metric tons
        "st": 907.185,      # short tons (2000 lbs)
        "lt": 1016.05       # long tons (2240 lbs)
    }
    _default_unit = "lb"
    _valid_units = set(_units.keys())
    
    def to_force(self, g: float = 9.80665) -> Force:
        """Convert mass to force under given acceleration.
        
        Args:
            g: Acceleration (default: standard gravity in m/s²)
        """
        mass_kg = self.to_unit("kg")
        force_n = mass_kg * g
        return Force(force_n, "N")

class PumpPressure(Pressure):
    """Specialized pressure class for pump operations."""
    
    def __init__(self, value: Union[float, int, Decimal], unit: str = "psi"):
        super().__init__(value, unit)
    
    def calculate_hydraulic_horsepower(self, flow_rate: 'FlowRate') -> float:
        """Calculate hydraulic horsepower.
        
        HHP = (P * Q) / 1714
        where P is pressure in psi and Q is flow rate in gpm
        """
        pressure_psi = self.to_unit("psi")
        flow_gpm = flow_rate.to_unit("gpm")
        return (pressure_psi * flow_gpm) / 1714
    
    def check_pressure_rating(self, rating: 'Pressure', safety_factor: float = 0.9) -> bool:
        """Check if pressure is within equipment rating."""
        return self.to_unit("psi") <= rating.to_unit("psi") * safety_factor
    
    def calculate_pressure_loss(self, flow_rate: 'FlowRate', length: Length, 
                              diameter: Diameter, fluid_properties: Dict) -> 'PumpPressure':
        """Calculate frictional pressure loss in pipe."""
        # Implementation depends on fluid model (Bingham Plastic, Power Law, etc.)
        # This is a simplified version
        pass

class SaltConcentration(PhysicalQuantity):
    """Salt concentration in drilling fluids."""
    
    _units = {
        "ppm": 1.0,         # parts per million
        "mg/L": 1.0,        # milligrams per liter
        "ppb": 0.001,       # parts per billion
        "percent": 10000.0, # weight percent
        "kg/m3": 1.0        # kilograms per cubic meter
    }
    _default_unit = "ppm"
    _valid_units = set(_units.keys())
    
    def calculate_chlorides(self) -> float:
        """Calculate chloride concentration from NaCl concentration."""
        nacl_ppm = self.to_unit("ppm")
        return nacl_ppm * 0.6067  # Cl/NaCl ratio
    
    def calculate_water_activity(self, temperature: float = 75.0) -> float:
        """Calculate water activity (approximate).
        
        Args:
            temperature: Temperature in °F
        """
        concentration = self.to_unit("percent")
        # Simplified calculation - actual value depends on temperature and pressure
        return 1.0 - (0.0335 * concentration)

class Stress(Pressure):
    """Mechanical stress calculations."""
    
    def calculate_strain(self, youngs_modulus: 'Pressure') -> float:
        """Calculate strain using Hooke's law."""
        return self.to_unit("psi") / youngs_modulus.to_unit("psi")
    
    def von_mises(self, stress2: 'Stress', stress3: 'Stress') -> 'Stress':
        """Calculate von Mises stress."""
        s1 = self.to_unit("psi")
        s2 = stress2.to_unit("psi")
        s3 = stress3.to_unit("psi")
        
        von_mises = math.sqrt(0.5 * ((s1 - s2)**2 + (s2 - s3)**2 + (s3 - s1)**2))
        return Stress(von_mises, "psi")

class Viscosity(PhysicalQuantity):
    """Fluid viscosity measurements."""
    
    _units = {
        "cP": 1.0,          # centipoise (common oilfield unit)
        "Pa.s": 1000.0,     # Pascal-seconds (SI unit)
        "P": 100.0,         # poise
        "lb.s/ft2": 47880.3 # pound second per square foot
    }
    _default_unit = "cP"
    _valid_units = set(_units.keys())
    
    def calculate_reynolds_number(self, density: Density, velocity: float, 
                                characteristic_length: Length) -> float:
        """Calculate Reynolds number."""
        viscosity_pas = self.to_unit("Pa.s")
        density_kgm3 = density.to_unit("kg/m3")
        length_m = characteristic_length.to_unit("m")
        
        return (density_kgm3 * velocity * length_m) / viscosity_pas
    
    def is_laminar_flow(self, re: float) -> bool:
        """Check if flow is laminar based on Reynolds number."""
        return re < 2300

class UnitCapacity(PhysicalQuantity):
    """Pipe and annular capacity calculations."""
    
    _units = {
        "bbl/ft": 1.0,      # barrels per foot
        "L/m": 1.547,       # liters per meter
        "gal/ft": 42.0,     # gallons per foot
        "m3/m": 0.001547    # cubic meters per meter
    }
    _default_unit = "bbl/ft"
    _valid_units = set(_units.keys())
    
    @classmethod
    def from_diameter(cls, diameter: Diameter) -> 'UnitCapacity':
        """Calculate capacity from internal diameter."""
        id_inch = diameter.to_unit("in")
        capacity_bbl_ft = (id_inch ** 2) / 1029.4
        return cls(capacity_bbl_ft, "bbl/ft")
    
    @classmethod
    def annular(cls, od: Diameter, id: Diameter) -> 'UnitCapacity':
        """Calculate annular capacity."""
        od_inch = od.to_unit("in")
        id_inch = id.to_unit("in")
        capacity_bbl_ft = (od_inch**2 - id_inch**2) / 1029.4
        return cls(capacity_bbl_ft, "bbl/ft")

class FlowRate(PhysicalQuantity):
    """Fluid flow rate measurements."""
    
    _units = {
        "m3/s": 1.0,        # cubic meters per second (SI)
        "gpm": 0.0630902,   # gallons per minute
        "bpm": 0.00265,     # barrels per minute
        "L/s": 0.001,       # liters per second
        "ft3/min": 0.000472 # cubic feet per minute
    }
    _default_unit = "gpm"
    _valid_units = set(_units.keys())
    
    def calculate_annular_velocity(self, capacity: UnitCapacity) -> float:
        """Calculate annular velocity in ft/min."""
        flow_bpm = self.to_unit("bpm")
        cap_bbl_ft = capacity.to_unit("bbl/ft")
        return (flow_bpm * 42.0) / cap_bbl_ft
    
    def is_hole_cleaning_adequate(self, hole_size: Diameter, 
                                angle: float = 90.0) -> bool:
        """Check if flow rate provides adequate hole cleaning.
        
        Args:
            hole_size: Hole diameter
            angle: Hole angle from vertical (degrees)
        """
        min_velocity = 120.0  # ft/min for vertical
        if angle < 45.0:
            min_velocity = 120.0
        elif angle < 60.0:
            min_velocity = 140.0
        else:
            min_velocity = 180.0
            
        capacity = UnitCapacity.from_diameter(hole_size)
        velocity = self.calculate_annular_velocity(capacity)
        
        return velocity >= min_velocity   
    
class WeightOnBit(Force):
    """Weight on bit measurements and calculations."""
    
    def __init__(self, value: Union[float, int, Decimal], unit: str = "klbf"):
        super().__init__(value, unit)
    
    def calculate_bit_pressure(self, bit_diameter: Diameter) -> Pressure:
        """Calculate pressure at bit face."""
        force_lbf = self.to_unit("lbf")
        area_in2 = bit_diameter.get_area().to_unit("in2")
        return Pressure(force_lbf / area_in2, "psi")
    
    def check_limit(self, bit_limit: float) -> bool:
        """Check if WOB is within bit rating.
        
        Args:
            bit_limit: Bit weight rating in klbf
        """
        return self.to_unit("klbf") <= bit_limit
    
    def recommended_range(bit_diameter: Diameter) -> Tuple['WeightOnBit', 'WeightOnBit']:
        """Get recommended WOB range based on bit size."""
        diameter_in = bit_diameter.to_unit("in")
        min_wob = diameter_in * 1.5  # typical 1.5-2.5 klb/inch rule of thumb
        max_wob = diameter_in * 2.5
        return (WeightOnBit(min_wob, "klbf"), WeightOnBit(max_wob, "klbf"))

class WeightPerLength(PhysicalQuantity):
    """Weight per unit length for drill string components."""
    
    _units = {
        "lb/ft": 1.0,       # pounds per foot
        "kg/m": 1.488164,   # kilograms per meter
        "N/m": 14.5939,     # newtons per meter
        "lb/in": 12.0       # pounds per inch
    }
    _default_unit = "lb/ft"
    _valid_units = set(_units.keys())
    
    def get_total_weight(self, length: Length) -> Weight:
        """Calculate total weight for given length."""
        weight_per_ft = self.to_unit("lb/ft")
        length_ft = length.to_unit("ft")
        return Weight(weight_per_ft * length_ft, "lbf")
    
    def buoyed_weight(self, mud_weight: MudWeight) -> 'WeightPerLength':
        """Calculate buoyed weight in drilling fluid."""
        weight_ppf = self.to_unit("lb/ft")
        mud_ppg = mud_weight.to_unit("ppg")
        buoyed_ppf = weight_ppf * (1 - (mud_ppg / 65.5))  # 65.5 ppg = steel density
        return WeightPerLength(buoyed_ppf, "lb/ft")

class Velocity(PhysicalQuantity):
    """Fluid velocity measurements."""
    
    _units = {
        "ft/min": 1.0,      # feet per minute (common in drilling)
        "ft/s": 60.0,       # feet per second
        "m/s": 196.85,      # meters per second
        "m/min": 3.28084    # meters per minute
    }
    _default_unit = "ft/min"
    _valid_units = set(_units.keys())
    
    def calculate_reynolds(self, diameter: Diameter, fluid_density: Density,
                         fluid_viscosity: Viscosity) -> float:
        """Calculate Reynolds number."""
        velocity_ms = self.to_unit("m/s")
        diameter_m = diameter.to_unit("m")
        density_kgm3 = fluid_density.to_unit("kg/m3")
        viscosity_pas = fluid_viscosity.to_unit("Pa.s")
        
        return (density_kgm3 * velocity_ms * diameter_m) / viscosity_pas
    
    def check_critical_velocity(self, minimum: float = 120.0) -> bool:
        """Check if velocity exceeds minimum for hole cleaning."""
        return self.to_unit("ft/min") >= minimum

class Volume(PhysicalQuantity):
    """Volume measurements with oilfield focus."""
    
    _units = {
        "bbl": 1.0,         # barrels (oil field standard)
        "gal": 42.0,        # US gallons
        "ft3": 5.614583,    # cubic feet
        "m3": 0.158987,     # cubic meters
        "L": 158.987        # liters
    }
    _default_unit = "bbl"
    _valid_units = set(_units.keys())
    
    def calculate_annular_displacement(self, depth: Length, od: Diameter, 
                                    id: Diameter) -> 'Volume':
        """Calculate annular volume."""
        od_in = od.to_unit("in")
        id_in = id.to_unit("in")
        depth_ft = depth.to_unit("ft")
        
        volume_bbl = ((od_in**2 - id_in**2) * depth_ft) / 1029.4
        return Volume(volume_bbl, "bbl")
    
    def calculate_displacement_time(self, flow_rate: FlowRate) -> float:
        """Calculate time to displace volume in minutes."""
        volume_bbl = self.to_unit("bbl")
        rate_bpm = flow_rate.to_unit("bpm")
        return volume_bbl / rate_bpm

class Temperature(PhysicalQuantity):
    """Temperature measurements with oilfield considerations."""
    
    _units = {
        "F": 1.0,           # Fahrenheit (common in US oilfield)
        "C": 1.8,           # Celsius
        "K": 1.8,           # Kelvin
        "R": 1.0            # Rankine
    }
    _default_unit = "F"
    _valid_units = set(_units.keys())
    
    def __init__(self, value: Union[float, int, Decimal], unit: str = "F"):
        # Handle absolute zero limits
        if unit == "K" and value < 0:
            raise ValueError("Temperature cannot be below absolute zero")
        if unit == "R" and value < 0:
            raise ValueError("Temperature cannot be below absolute zero")
        if unit == "C" and value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero")
        if unit == "F" and value < -459.67:
            raise ValueError("Temperature cannot be below absolute zero")
            
        super().__init__(value, unit)
    
    def to_unit(self, target_unit: str) -> float:
        """Convert between temperature units with proper offsets."""
        if self.unit == target_unit:
            return self.value
            
        # Convert to Fahrenheit first
        if self.unit == "C":
            f_temp = (self.value * 9/5) + 32
        elif self.unit == "K":
            f_temp = (self.value * 9/5) - 459.67
        elif self.unit == "R":
            f_temp = self.value - 459.67
        else:  # Already Fahrenheit
            f_temp = self.value
            
        # Convert from Fahrenheit to target
        if target_unit == "C":
            return (f_temp - 32) * 5/9
        elif target_unit == "K":
            return ((f_temp + 459.67) * 5/9)
        elif target_unit == "R":
            return f_temp + 459.67
        else:  # Return Fahrenheit
            return f_temp
    
    def calculate_gradient(self, depth: Length) -> float:
        """Calculate temperature gradient in °F/ft."""
        temp_f = self.to_unit("F")
        depth_ft = depth.to_unit("ft")
        return temp_f / depth_ft

class GasFlowRate(FlowRate):
    """Gas flow rate measurements."""
    
    _units = {
        "scf/min": 1.0,     # standard cubic feet per minute
        "MMscf/d": 694.444, # million standard cubic feet per day
        "m3/min": 0.0283,   # cubic meters per minute
        "scf/d": 0.000694   # standard cubic feet per day
    }
    _default_unit = "scf/min"
    _valid_units = set(_units.keys())
    
    def to_mass_rate(self, gas_gravity: float = 1.0) -> float:
        """Convert to mass flow rate (lb/hr).
        
        Args:
            gas_gravity: Specific gravity relative to air (default=1.0)
        """
        scfm = self.to_unit("scf/min")
        # Standard conditions mass flow calculation
        return scfm * gas_gravity * 0.0764 * 60  # lb/hr

    def calculate_pressure_drop(self, length: Length, diameter: Diameter,
                              inlet_pressure: Pressure, temperature: Temperature,
                              gas_gravity: float = 1.0) -> Pressure:
        """Calculate pressure drop in gas flow line."""
        # Implementation would use appropriate gas flow equation
        # (e.g., Weymouth, Panhandle, etc.)
        pass

class ROP(PhysicalQuantity):
    """Rate of Penetration measurements."""
    
    _units = {
        "ft/hr": 1.0,       # feet per hour (common US)
        "m/hr": 0.3048,     # meters per hour
        "ft/min": 60.0,     # feet per minute
        "m/min": 0.3048     # meters per minute
    }
    _default_unit = "ft/hr"
    _valid_units = set(_units.keys())
    
    def calculate_drilling_time(self, length: Length) -> float:
        """Calculate time to drill given length in hours."""
        rate_fthr = self.to_unit("ft/hr")
        length_ft = length.to_unit("ft")
        return length_ft / rate_fthr
    
    def calculate_mse(self, wob: WeightOnBit, rpm: 'RPM', 
                     torque: Torque, bit_diameter: Diameter) -> Pressure:
        """Calculate Mechanical Specific Energy."""
        # MSE = (480 × T × N)/(π × D² × ROP) + (4 × WOB)/(π × D²)
        d_inches = bit_diameter.to_unit("in")
        area = math.pi * (d_inches ** 2) / 4
        
        rotation_term = (480 * torque.to_unit("ftlb") * rpm.to_unit("rpm")) / \
                       (math.pi * d_inches**2 * self.to_unit("ft/hr"))
        wob_term = (4 * wob.to_unit("lbf")) / (math.pi * d_inches**2)
        
        return Pressure(rotation_term + wob_term, "psi")

class RPM(PhysicalQuantity):
    """Rotational speed measurements."""
    
    _units = {
        "rpm": 1.0,         # revolutions per minute
        "rps": 60.0,        # revolutions per second
        "rad/s": 9.549297,  # radians per second
        "deg/s": 0.166667   # degrees per second
    }
    _default_unit = "rpm"
    _valid_units = set(_units.keys())
    
    def calculate_tip_speed(self, diameter: Diameter) -> Velocity:
        """Calculate bit/tool tip speed."""
        rpm_value = self.to_unit("rpm")
        diameter_ft = diameter.to_unit("ft")
        tip_speed = math.pi * diameter_ft * rpm_value
        return Velocity(tip_speed, "ft/min")
    
    def check_motor_rating(self, rating: float) -> bool:
        """Check if RPM is within motor rating."""
        return self.to_unit("rpm") <= rating
    
    def calculate_slip_ratio(self, motor_rpm: 'RPM') -> float:
        """Calculate slip ratio for mud motor."""
        return 1 - (self.to_unit("rpm") / motor_rpm.to_unit("rpm"))

class Density(PhysicalQuantity):
    """Enhanced density measurements for drilling fluids and materials."""
    
    _units = {
        "kg/m3": 1.0,          # kilograms per cubic meter (SI)
        "ppg": 119.826427,     # pounds per gallon (US oilfield)
        "lb/ft3": 16.0185,     # pounds per cubic foot
        "g/cm3": 1000.0,       # grams per cubic centimeter
        "sg": 1000.0,          # specific gravity (relative to water)
        "psi/ft": 0.052,       # pressure gradient
        "kg/L": 1000.0,        # kilograms per liter
        "lb/bbl": 2.853,       # pounds per barrel
    }
    _default_unit = "ppg"      # Common in oil field
    _valid_units = set(_units.keys())
    
    def to_pressure_gradient(self) -> float:
        """Convert density to pressure gradient in psi/ft."""
        ppg = self.to_unit("ppg")
        return ppg * 0.052
    
    def calculate_hydrostatic_pressure(self, depth: Length) -> Pressure:
        """Calculate hydrostatic pressure at given depth."""
        gradient = self.to_pressure_gradient()
        depth_ft = depth.to_unit("ft")
        return Pressure(gradient * depth_ft, "psi")
    
    def get_equivalent_mud_weight(self) -> MudWeight:
        """Convert to equivalent mud weight."""
        ppg = self.to_unit("ppg")
        return MudWeight(ppg, "ppg")
    
    def check_barite_sag_risk(self) -> str:
        """Evaluate risk of barite sag."""
        ppg = self.to_unit("ppg")
        if ppg < 12.0:
            return "Low Risk"
        elif ppg < 16.0:
            return "Moderate Risk - Monitor"
        else:
            return "High Risk - Implement sag mitigation"
    
    def calculate_equivalent_density(self, additional_pressure: Pressure, 
                                   depth: Length) -> 'Density':
        """Calculate equivalent density including additional pressure."""
        base_pressure = self.calculate_hydrostatic_pressure(depth)
        total_pressure = base_pressure.to_unit("psi") + additional_pressure.to_unit("psi")
        equiv_ppg = (total_pressure / depth.to_unit("ft")) / 0.052
        return Density(equiv_ppg, "ppg")

class Power(PhysicalQuantity):
    """Power measurements for drilling operations."""
    
    _units = {
        "hp": 1.0,          # horsepower (common US oilfield)
        "kW": 0.7457,       # kilowatts
        "W": 0.0007457,     # watts
        "ftlb/min": 33000,  # foot-pounds per minute
        "BTU/hr": 2544.43   # British thermal units per hour
    }
    _default_unit = "hp"
    _valid_units = set(_units.keys())
    
    def calculate_hydraulic_hp(self, pressure: Pressure, flow_rate: FlowRate) -> 'Power':
        """Calculate hydraulic horsepower.
        
        HHP = (P * Q) / 1714
        where P is pressure in psi and Q is flow rate in gpm
        """
        pressure_psi = pressure.to_unit("psi")
        flow_gpm = flow_rate.to_unit("gpm")
        hhp = (pressure_psi * flow_gpm) / 1714
        return Power(hhp, "hp")
    
    def calculate_rotary_power(self, torque: Torque, rpm: RPM) -> 'Power':
        """Calculate power from torque and RPM."""
        torque_ftlb = torque.to_unit("ftlb")
        rpm_value = rpm.to_unit("rpm")
        hp = (torque_ftlb * rpm_value) / 5252
        return Power(hp, "hp")
    
    def check_motor_rating(self, required_power: 'Power', 
                          safety_factor: float = 1.5) -> bool:
        """Check if power meets requirement with safety factor."""
        return self.to_unit("hp") >= required_power.to_unit("hp") * safety_factor

class SurfaceTension(PhysicalQuantity):
    """Surface tension measurements for drilling fluids."""
    
    _units = {
        "N/m": 1.0,         # Newtons per meter (SI)
        "dyne/cm": 0.001,   # dynes per centimeter
        "mN/m": 0.001,      # milliNewtons per meter
        "lbf/ft": 14.5939   # pounds force per foot
    }
    _default_unit = "dyne/cm"  # Common in lab measurements
    _valid_units = set(_units.keys())
    
    def calculate_capillary_pressure(self, diameter: Diameter, 
                                   contact_angle: float = 0) -> Pressure:
        """Calculate capillary pressure.
        
        Args:
            diameter: Pore/tube diameter
            contact_angle: Contact angle in degrees (default=0)
        """
        surface_tension_nm = self.to_unit("N/m")
        diameter_m = diameter.to_unit("m")
        theta_rad = math.radians(contact_angle)
        
        # Pc = (4 * γ * cos θ) / d
        pc_pa = (4 * surface_tension_nm * math.cos(theta_rad)) / diameter_m
        return Pressure(pc_pa / 6894.76, "psi")  # Convert Pa to psi
    
    def estimate_emulsion_stability(self) -> str:
        """Estimate emulsion stability based on surface tension."""
        dynes = self.to_unit("dyne/cm")
        if dynes < 20:
            return "Unstable - High risk of separation"
        elif dynes < 30:
            return "Moderately stable"
        else:
            return "Stable emulsion"

class Compressibility(PhysicalQuantity):
    """Compressibility measurements for fluids and formations."""
    
    _units = {
        "1/psi": 1.0,           # inverse psi (common oilfield)
        "1/Pa": 6.894757e-6,    # inverse Pascal
        "1/bar": 0.06894757,    # inverse bar
        "1/kPa": 6.894757e-3    # inverse kiloPascal
    }
    _default_unit = "1/psi"
    _valid_units = set(_units.keys())
    
    def calculate_volume_change(self, initial_volume: Volume, 
                              pressure_change: Pressure) -> Volume:
        """Calculate volume change due to pressure change."""
        comp_per_psi = self.to_unit("1/psi")
        delta_p = pressure_change.to_unit("psi")
        initial_bbl = initial_volume.to_unit("bbl")
        
        delta_v = initial_bbl * comp_per_psi * delta_p
        return Volume(delta_v, "bbl")
    
    def estimate_formation_strength(self) -> str:
        """Estimate formation competency based on compressibility."""
        comp_per_psi = self.to_unit("1/psi")
        if comp_per_psi < 1e-6:
            return "Hard/Competent Formation"
        elif comp_per_psi < 3e-6:
            return "Medium Strength Formation"
        else:
            return "Soft/Weak Formation"

class Voltage(PhysicalQuantity):
    """Voltage measurements for electrical equipment."""
    
    _units = {
        "V": 1.0,           # volts
        "kV": 1000.0,       # kilovolts
        "mV": 0.001,        # millivolts
        "uV": 0.000001     # microvolts
    }
    _default_unit = "V"
    _valid_units = set(_units.keys())
    
    def calculate_power(self, current: 'Current', 
                       power_factor: float = 1.0) -> Power:
        """Calculate electrical power.
        
        Args:
            current: Current in amperes
            power_factor: Power factor (default=1.0 for DC)
        """
        volts = self.to_unit("V")
        amps = current.to_unit("A")
        watts = volts * amps * power_factor
        return Power(watts/745.7, "hp")  # Convert to horsepower
    
    def check_motor_rating(self, rating: 'Voltage', 
                          tolerance: float = 0.1) -> bool:
        """Check if voltage is within motor rating ±tolerance."""
        nominal = rating.to_unit("V")
        actual = self.to_unit("V")
        return abs(actual - nominal) <= (nominal * tolerance)

class Current(PhysicalQuantity):
    """Current measurements for electrical equipment."""
    
    _units = {
        "A": 1.0,           # amperes
        "mA": 0.001,        # milliamperes
        "kA": 1000.0,       # kiloamperes
        "uA": 0.000001     # microamperes
    }
    _default_unit = "A"
    _valid_units = set(_units.keys())
    
    def calculate_heating(self, resistance: float, time: float) -> Energy:
        """Calculate heating energy (I²Rt).
        
        Args:
            resistance: Resistance in ohms
            time: Time in seconds
        """
        amps = self.to_unit("A")
        # E = I²Rt (in joules)
        energy_j = (amps ** 2) * resistance * time
        return Energy(energy_j, "J")
    
    def check_wire_rating(self, rating: float, 
                         derating_factor: float = 0.8) -> bool:
        """Check if current is within wire ampacity."""
        return self.to_unit("A") <= (rating * derating_factor)
    
    def calculate_torque_factor(self, nominal_current: 'Current') -> float:
        """Calculate motor torque factor based on current draw."""
        return self.to_unit("A") / nominal_current.to_unit("A")

class Pressure(PhysicalQuantity):
    """Enhanced pressure measurements for well and reservoir analysis."""
    
    _units = {
        "psi": 1.0,         # pounds per square inch (oilfield standard)
        "kPa": 6.894757,    # kilopascals
        "MPa": 6894.757,    # megapascals
        "bar": 68.94757,    # bars
        "atm": 68.046,      # atmospheres
        "kg/cm2": 70.307,   # kilograms per square centimeter
        "psi/ft": 1.0,      # pressure gradient
        "kPa/m": 22.62      # pressure gradient (metric)
    }
    _default_unit = "psi"
    _valid_units = set(_units.keys())
    
    def calculate_gradient(self, depth: Length) -> float:
        """Calculate pressure gradient."""
        psi = self.to_unit("psi")
        ft = depth.to_unit("ft")
        return psi / ft
    
    def is_normal_pressure(self, depth: Length, 
                          tolerance: float = 0.1) -> bool:
        """Check if pressure is within normal pressure range.
        
        Normal pressure gradient ≈ 0.433 psi/ft for freshwater
        """
        gradient = self.calculate_gradient(depth)
        return abs(gradient - 0.433) <= tolerance
    
    def get_overbalance(self, pore_pressure: 'Pressure') -> 'Pressure':
        """Calculate overbalance pressure."""
        return Pressure(self.to_unit("psi") - pore_pressure.to_unit("psi"), "psi")
    
    def calculate_fracture_gradient(self, depth: Length, 
                                  poisson_ratio: float = 0.25) -> float:
        """Calculate fracture gradient using simplified method."""
        overburden_gradient = 1.0  # Typical value in psi/ft
        pore_gradient = self.calculate_gradient(depth)
        
        # Using simplified Hubbert-Willis equation
        frac_gradient = ((poisson_ratio / (1 - poisson_ratio)) * 
                        (overburden_gradient - pore_gradient) + pore_gradient)
        return frac_gradient
    
    def to_mud_weight(self) -> MudWeight:
        """Convert pressure gradient to equivalent mud weight."""
        gradient = self.calculate_gradient(Length(1, "ft"))
        return MudWeight(gradient / 0.052, "ppg")

class Porosity(PhysicalQuantity):
    """Porosity measurements for reservoir characterization."""
    
    _units = {
        "fraction": 1.0,    # decimal fraction
        "percent": 0.01,    # percentage
        "v/v": 1.0         # volume/volume (same as fraction)
    }
    _default_unit = "fraction"
    _valid_units = set(_units.keys())
    
    def __init__(self, value: Union[float, int, Decimal], unit: str = "fraction"):
        super().__init__(value, unit)
        # Validate porosity is between 0 and 1 (or 0-100 for percent)
        if unit == "fraction" and (value < 0 or value > 1):
            raise ValueError("Porosity fraction must be between 0 and 1")
        elif unit == "percent" and (value < 0 or value > 100):
            raise ValueError("Porosity percentage must be between 0 and 100")
    
    def calculate_pore_volume(self, bulk_volume: Volume) -> Volume:
        """Calculate pore volume from bulk volume."""
        fraction = self.to_unit("fraction")
        return Volume(bulk_volume.value * fraction, bulk_volume.unit)
    
    def estimate_compaction_trend(self, depth: Length) -> 'Porosity':
        """Estimate porosity at depth using Athy's formula.
        
        φ = φ₀ * e^(-kz)
        where φ₀ is surface porosity and k is compaction coefficient
        """
        phi0 = 0.4  # Typical surface porosity
        k = 0.00025  # Typical compaction coefficient (1/ft)
        depth_ft = depth.to_unit("ft")
        new_porosity = phi0 * math.exp(-k * depth_ft)
        return Porosity(new_porosity, "fraction")
    
    def classify_reservoir_quality(self) -> str:
        """Classify reservoir quality based on porosity."""
        porosity_percent = self.to_unit("percent")
        if porosity_percent < 5:
            return "Poor"
        elif porosity_percent < 10:
            return "Fair"
        elif porosity_percent < 15:
            return "Good"
        elif porosity_percent < 20:
            return "Very Good"
        else:
            return "Excellent"

class Permeability(PhysicalQuantity):
    """Permeability measurements for reservoir characterization."""
    
    _units = {
        "md": 1.0,              # millidarcy (oilfield standard)
        "D": 1000.0,            # darcy
        "m2": 9.869233e-10,     # square meters
        "um2": 9.869233e-4      # square micrometers
    }
    _default_unit = "md"
    _valid_units = set(_units.keys())
    
    def calculate_flow_rate(self, delta_pressure: Pressure, length: Length,
                           viscosity: Viscosity, area: Area) -> FlowRate:
        """Calculate flow rate using Darcy's law."""
        k = self.to_unit("m2")
        dp = delta_pressure.to_unit("Pa")
        L = length.to_unit("m")
        mu = viscosity.to_unit("Pa.s")
        A = area.to_unit("m2")
        
        # Q = -(k*A/μ) * (dP/dL)
        flow_m3s = (k * A * dp) / (mu * L)
        return FlowRate(flow_m3s * 60, "m3/min")
    
    def estimate_skin_factor(self, observed_k: 'Permeability', 
                           radius: Length) -> float:
        """Estimate skin factor from permeability contrast."""
        k_ratio = self.to_unit("md") / observed_k.to_unit("md")
        radius_ft = radius.to_unit("ft")
        return math.log(k_ratio) + 2  # Simplified skin calculation
    
    def classify_reservoir_quality(self) -> str:
        """Classify reservoir quality based on permeability."""
        k_md = self.to_unit("md")
        if k_md < 1:
            return "Poor"
        elif k_md < 10:
            return "Fair"
        elif k_md < 50:
            return "Good"
        elif k_md < 250:
            return "Very Good"
        else:
            return "Excellent"

class GasOilRatio(PhysicalQuantity):
    """Gas-Oil Ratio measurements for reservoir fluid characterization."""
    
    _units = {
        "scf/bbl": 1.0,     # standard cubic feet per barrel
        "m3/m3": 5.6146,    # cubic meters gas per cubic meter oil
        "scf/stb": 1.0,     # standard cubic feet per stock tank barrel
        "L/L": 5.6146       # liters gas per liter oil
    }
    _default_unit = "scf/bbl"
    _valid_units = set(_units.keys())
    
    def estimate_bubble_point(self, temperature: Temperature,
                            api_gravity: float) -> Pressure:
        """Estimate bubble point pressure using Standing's correlation."""
        gor = self.to_unit("scf/bbl")
        temp_f = temperature.to_unit("F")
        
        # Standing's correlation
        pb = 18.2 * ((gor/api_gravity)**0.83 * 10**(0.00091 * temp_f - 0.0125 * api_gravity) - 1.4)
        return Pressure(pb, "psi")
    
    def calculate_gas_volume(self, oil_volume: Volume) -> Volume:
        """Calculate gas volume at standard conditions."""
        gor = self.to_unit("scf/bbl")
        oil_bbl = oil_volume.to_unit("bbl")
        gas_scf = gor * oil_bbl
        return Volume(gas_scf, "ft3")
    
    def classify_reservoir_fluid(self) -> str:
        """Classify reservoir fluid type based on GOR."""
        gor = self.to_unit("scf/bbl")
        if gor < 2000:
            return "Black Oil"
        elif gor < 3300:
            return "Volatile Oil"
        else:
            return "Gas Condensate"

class Acceleration(PhysicalQuantity):
    """Acceleration measurements for drilling dynamics."""
    
    _units = {
        "g": 1.0,           # gravitational acceleration (9.81 m/s²)
        "m/s2": 9.80665,    # meters per second squared
        "ft/s2": 32.174,    # feet per second squared
        "in/s2": 386.089    # inches per second squared
    }
    _default_unit = "g"
    _valid_units = set(_units.keys())
    
    def calculate_force(self, mass: Mass) -> Force:
        """Calculate force using F = ma."""
        acc_ms2 = self.to_unit("m/s2")
        mass_kg = mass.to_unit("kg")
        force_n = mass_kg * acc_ms2
        return Force(force_n, "N")
    
    def calculate_shock_load(self, base_load: Force) -> Force:
        """Calculate shock load on equipment."""
        g_value = self.to_unit("g")
        base_n = base_load.to_unit("N")
        return Force(base_n * g_value, "N")
    
    def classify_vibration_severity(self) -> str:
        """Classify vibration severity based on acceleration."""
        g_value = self.to_unit("g")
        if g_value < 0.5:
            return "Normal"
        elif g_value < 2.0:
            return "Moderate"
        elif g_value < 4.0:
            return "Severe"
        else:
            return "Critical - Risk of Equipment Damage"
    
    def estimate_displacement(self, frequency: float) -> Length:
        """Estimate displacement amplitude from acceleration.
        
        Args:
            frequency: Vibration frequency in Hz
        """
        acc_ms2 = self.to_unit("m/s2")
        # d = a/(2πf)²
        displacement_m = acc_ms2 / ((2 * math.pi * frequency) ** 2)
        return Length(displacement_m, "m")

# Add relevant exceptions
class QuantityError(Exception):
    """Base exception for quantity-related errors."""
    pass

class UnitError(QuantityError):
    """Raised when there's an issue with units."""
    pass

class ConversionError(QuantityError):
    """Raised when there's an error in unit conversion."""
    pass

# Add utility functions
def validate_positive(quantity: PhysicalQuantity) -> bool:
    """Validate that a quantity is positive."""
    return quantity.value > 0

def validate_non_negative(quantity: PhysicalQuantity) -> bool:
    """Validate that a quantity is non-negative."""
    return quantity.value >= 0

def convert_to_base_units(quantities: Dict[str, PhysicalQuantity]) -> Dict[str, float]:
    """Convert a dictionary of quantities to their base units."""
    return {key: q.to_unit(q._default_unit) for key, q in quantities.items()}

def calculate_motor_efficiency(input_power: Power, output_power: Power) -> float:
    """Calculate motor efficiency as percentage."""
    return (output_power.to_unit("hp") / input_power.to_unit("hp")) * 100

def check_phase_balance(currents: List[Current], 
                       max_imbalance: float = 0.02) -> bool:
    """Check if three-phase currents are balanced within tolerance."""
    if len(currents) != 3:
        raise ValueError("Three phase currents required")
        
    values = [c.to_unit("A") for c in currents]
    avg = sum(values) / 3
    max_deviation = max(abs(v - avg) for v in values)
    return (max_deviation / avg) <= max_imbalance

# Utility functions for reservoir analysis
def calculate_recovery_factor(ooip: Volume, cumulative_production: Volume) -> float:
    """Calculate recovery factor as percentage."""
    return (cumulative_production.to_unit("bbl") / ooip.to_unit("bbl")) * 100

def estimate_original_oil_in_place(bulk_volume: Volume, 
                                 porosity: Porosity,
                                 water_saturation: float) -> Volume:
    """Calculate OOIP using volumetric method."""
    bv_bbl = bulk_volume.to_unit("bbl")
    pore_volume = bv_bbl * porosity.to_unit("fraction")
    oil_volume = pore_volume * (1 - water_saturation)
    return Volume(oil_volume, "bbl")

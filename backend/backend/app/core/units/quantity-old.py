from abc import ABC, abstractmethod
from typing import Dict, Union, List, Optional, TypeVar, Generic, Tuple
from dataclasses import dataclass
import math
from enum import Enum
from decimal import Decimal, ROUND_HALF_UP
import uncertainties
from uncertainties import ufloat

T = TypeVar('T', bound='Quantity')

class UnitSystem(Enum):
    """Enum to define different unit systems"""
    METRIC = "metric"
    IMPERIAL = "imperial"
    FIELD = "field"

class DisplayFormat(Enum):
    """Enum for different display format options"""
    PLAIN = "plain"  # Simple number
    SCIENTIFIC = "scientific"  # Scientific notation
    ENGINEERING = "engineering"  # Engineering notation
    COMPACT = "compact"  # Compact notation (e.g., 1.2k, 1.3M)

@dataclass
class UnitDefinition:
    """Data class to hold unit definition information"""
    symbol: str
    name: str
    system: UnitSystem
    conversion_factor: float
    is_base: bool = False
    min_value: Optional[float] = None  # Minimum allowed value
    max_value: Optional[float] = None  # Maximum allowed value
    uncertainty: Optional[float] = None  # Default uncertainty

@dataclass
class Uncertainty:
    """Data class to hold uncertainty information"""
    value: float
    absolute_error: float
    relative_error: float
    confidence_level: float = 0.95

class Quantity(ABC):
    """Enhanced abstract base class for all quantity types"""
    
    def __init__(self, value: float, unit: str, uncertainty: Optional[float] = None):
        """Initialize a quantity with value, unit and optional uncertainty"""
        self._validate_unit(unit)
        self._validate_value(value)
        
        self.nominal_value = float(value)
        self.unit = unit
        self._ufloat = ufloat(value, uncertainty if uncertainty is not None else 0)
        
        # Initialize formatting options
        self.display_format = DisplayFormat.PLAIN
        self.decimal_places = 2
        self.significant_figures = None

    @property
    @abstractmethod
    def conversion_factors(self) -> Dict[str, float]:
        """Dictionary of conversion factors for this quantity type"""
        pass

    @property
    @abstractmethod
    def valid_range(self) -> Tuple[Optional[float], Optional[float]]:
        """Valid range for this quantity type (min, max)"""
        return (None, None)  # Default to no range limitations

    @property
    def value(self) -> float:
        """Get the nominal value"""
        return self.nominal_value

    @property
    def uncertainty(self) -> float:
        """Get the uncertainty value"""
        return self._ufloat.std_dev

    @property
    def relative_uncertainty(self) -> float:
        """Get the relative uncertainty"""
        return self.uncertainty / self.value if self.value != 0 else float('inf')

    def set_uncertainty(self, absolute_error: float, confidence_level: float = 0.95) -> None:
        """Set the uncertainty of the measurement"""
        self._ufloat = ufloat(self.value, absolute_error)

    def _validate_unit(self, unit: str) -> None:
        """Validate the unit"""
        if unit not in self.conversion_factors:
            valid_units = ", ".join(self.conversion_factors.keys())
            raise ValueError(f"Invalid unit '{unit}'. Valid units are: {valid_units}")

    def _validate_value(self, value: float) -> None:
        """Validate the value against physical constraints"""
        min_val, max_val = self.valid_range
        if min_val is not None and value < min_val:
            raise ValueError(f"Value {value} is below minimum allowed value {min_val}")
        if max_val is not None and value > max_val:
            raise ValueError(f"Value {value} is above maximum allowed value {max_val}")

    def set_display_format(self, format: DisplayFormat, decimal_places: int = 2, 
                          significant_figures: Optional[int] = None) -> None:
        """Set the display format for the quantity"""
        self.display_format = format
        self.decimal_places = decimal_places
        self.significant_figures = significant_figures

    def _format_value(self, value: float) -> str:
        """Format a value according to current display settings"""
        if self.display_format == DisplayFormat.SCIENTIFIC:
            return f"{value:.{self.decimal_places}e}"
        elif self.display_format == DisplayFormat.ENGINEERING:
            exp = int(math.floor(math.log10(abs(value)) if value != 0 else 0))
            eng_exp = exp - (exp % 3)
            mantissa = value / (10 ** eng_exp)
            return f"{mantissa:.{self.decimal_places}f}e{eng_exp}"
        elif self.display_format == DisplayFormat.COMPACT:
            if abs(value) >= 1e9:
                return f"{value/1e9:.{self.decimal_places}f}B"
            elif abs(value) >= 1e6:
                return f"{value/1e6:.{self.decimal_places}f}M"
            elif abs(value) >= 1e3:
                return f"{value/1e3:.{self.decimal_places}f}k"
            else:
                return f"{value:.{self.decimal_places}f}"
        else:  # DisplayFormat.PLAIN
            if self.significant_figures is not None:
                return f"{value:.{self.significant_figures}g}"
            return f"{value:.{self.decimal_places}f}"

    def __str__(self) -> str:
        """Enhanced string representation with formatting"""
        value_str = self._format_value(self.value)
        if self.uncertainty > 0:
            uncertainty_str = self._format_value(self.uncertainty)
            return f"{value_str} ± {uncertainty_str} {self.unit}"
        return f"{value_str} {self.unit}"

    def __repr__(self) -> str:
        """Detailed string representation"""
        return (f"{self.__class__.__name__}(value={self.value}, unit='{self.unit}', "
                f"uncertainty={self.uncertainty})")

    # Enhanced mathematical operations
    def __add__(self, other: Union[T, float]) -> T:
        """Add quantities or scalar"""
        if isinstance(other, (int, float)):
            return self.__class__(self.value + other, self.unit, self.uncertainty)
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot add {type(self)} and {type(other)}")
        
        # Convert other to this unit and add uncertainties
        other_value = other.to_unit(self.unit)
        result = self._ufloat + other._ufloat
        return self.__class__(float(result.nominal_value), self.unit, float(result.std_dev))

    def __radd__(self, other: float) -> T:
        """Reverse add for scalar + quantity"""
        return self.__add__(other)

    def __sub__(self, other: Union[T, float]) -> T:
        """Subtract quantities or scalar"""
        if isinstance(other, (int, float)):
            return self.__class__(self.value - other, self.unit, self.uncertainty)
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot subtract {type(self)} and {type(other)}")
        
        other_value = other.to_unit(self.unit)
        result = self._ufloat - other._ufloat
        return self.__class__(float(result.nominal_value), self.unit, float(result.std_dev))

    def __rsub__(self, other: float) -> T:
        """Reverse subtract for scalar - quantity"""
        return self.__class__(other - self.value, self.unit, self.uncertainty)

    def __mul__(self, other: Union[T, float]) -> T:
        """Multiply by scalar or compatible quantity"""
        if isinstance(other, (int, float)):
            result = self._ufloat * other
            return self.__class__(float(result.nominal_value), self.unit, float(result.std_dev))
        raise TypeError(f"Cannot multiply {type(self)} by {type(other)}")

    def __rmul__(self, other: float) -> T:
        """Reverse multiply for scalar * quantity"""
        return self.__mul__(other)

    def __truediv__(self, other: Union[T, float]) -> T:
        """Divide by scalar or compatible quantity"""
        if isinstance(other, (int, float)):
            if other == 0:
                raise ValueError("Cannot divide by zero")
            result = self._ufloat / other
            return self.__class__(float(result.nominal_value), self.unit, float(result.std_dev))
        raise TypeError(f"Cannot divide {type(self)} by {type(other)}")

    def __rtruediv__(self, other: float) -> T:
        """Reverse divide for scalar / quantity"""
        if self.value == 0:
            raise ValueError("Cannot divide by zero")
        result = other / self._ufloat
        return self.__class__(float(result.nominal_value), self.unit, float(result.std_dev))

    def __pow__(self, power: float) -> T:
        """Raise quantity to a power"""
        result = self._ufloat ** power
        return self.__class__(float(result.nominal_value), self.unit, float(result.std_dev))

    def sqrt(self) -> T:
        """Square root of quantity"""
        return self.__pow__(0.5)

    def abs(self) -> T:
        """Absolute value of quantity"""
        return self.__class__(abs(self.value), self.unit, self.uncertainty)

    # Comparison operations with tolerance
    def __eq__(self, other: object) -> bool:
        """Equal within tolerance"""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return math.isclose(self.to_unit(self.base_unit), 
                          other.to_unit(self.base_unit),
                          rel_tol=1e-9,
                          abs_tol=1e-9)

    def __lt__(self, other: T) -> bool:
        """Less than comparison"""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot compare {type(self)} with {type(other)}")
        return self.to_unit(self.base_unit) < other.to_unit(self.base_unit)

    def __le__(self, other: T) -> bool:
        """Less than or equal comparison"""
        return self < other or self == other

    # Statistical methods
    @classmethod
    def from_measurements(cls, measurements: List[T]) -> T:
        """Create quantity from list of measurements with uncertainty"""
        if not measurements:
            raise ValueError("Cannot create quantity from empty measurement list")
        
        # Convert all measurements to base unit
        base_values = [m.to_unit(measurements[0].base_unit) for m in measurements]
        
        # Calculate mean and standard deviation
        mean = sum(base_values) / len(base_values)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in base_values) / (len(base_values) - 1))
        
        return cls(mean, measurements[0].base_unit, std_dev)

class Depth(Quantity):
    """Represents depth measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "ft": 1,  # Base unit for field operations
            "ftSe": 1.000017338,
            "cm": 30.48,
            "ftUS": 0.999998,
            "in": 12,
            "m": 0.3048,
            "mm": 304.8,
            "km": 0.0003048,
            "mi": 0.000189394,
            "yd": 0.333333333,
        }

    @property
    def valid_range(self) -> Tuple[Optional[float], Optional[float]]:
        """Depth cannot be negative in well engineering"""
        return (0, None)

    def calculate_true_vertical_depth(self, angle: 'Azimuth') -> 'Depth':
        """Calculate true vertical depth given an inclination angle
        
        Args:
            angle: Inclination angle from vertical
            
        Returns:
            TVD as a Depth object
        """
        angle_rad = angle.to_unit("rad")
        tvd = self.value * math.cos(angle_rad)
        return Depth(tvd, self.unit, self.uncertainty)

    def calculate_horizontal_displacement(self, tvd: 'Depth') -> 'Length':
        """Calculate horizontal displacement given TVD
        
        Args:
            tvd: True Vertical Depth
            
        Returns:
            Horizontal displacement as a Length object
        """
        # Convert both to same unit
        tvd_value = tvd.to_unit(self.unit)
        # Using Pythagorean theorem
        hd = math.sqrt(self.value**2 - tvd_value**2)
        return Length(hd, self.unit, self.uncertainty)

class Length(Quantity):
    """Represents linear measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "m": 1,  # Base unit
            "cm": 100,
            "mm": 1000,
            "km": 0.001,
            "in": 39.3701,
            "ft": 3.28084,
            "yd": 1.09361,
            "mi": 0.000621371
        }

    def to_metric(self) -> 'Length':
        """Convert to metric (meters)"""
        return Length(self.to_unit("m"), "m", self.uncertainty)

    def to_imperial(self) -> 'Length':
        """Convert to imperial (feet)"""
        return Length(self.to_unit("ft"), "ft", self.uncertainty)

class Diameter(Quantity):
    """Represents diameter measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "in": 1,  # Base unit for wellbore/pipe diameter
            "cm": 2.54,
            "ft": 0.0833333333,
            "m": 0.0254,
            "mm": 25.4
        }

    @property
    def valid_range(self) -> Tuple[Optional[float], Optional[float]]:
        """Diameter must be positive"""
        return (0, None)

    def calculate_area(self) -> 'Area':
        """Calculate cross-sectional area"""
        # Convert to base unit (inches) for calculation
        radius = self.to_unit("in") / 2
        area_sq_in = math.pi * radius**2
        return Area(area_sq_in, "in2", self.uncertainty * 2 if self.uncertainty else None)

    def calculate_circumference(self) -> 'Length':
        """Calculate circumference"""
        # Convert to base unit (inches) for calculation
        circumference = math.pi * self.to_unit("in")
        return Length(circumference, "in", self.uncertainty * math.pi if self.uncertainty else None)

class Azimuth(Quantity):
    """Represents azimuthal measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "deg": 1,  # Base unit
            "rad": math.pi / 180,
            "grad": 1.111111111  # 100 grads = 90 degrees
        }

    @property
    def valid_range(self) -> Tuple[Optional[float], Optional[float]]:
        """Azimuth should be between 0 and 360 degrees"""
        return (0, 360)

    def __init__(self, value: float, unit: str, uncertainty: Optional[float] = None):
        """Initialize and normalize azimuth"""
        super().__init__(value, unit, uncertainty)
        self.normalize()

    def normalize(self) -> None:
        """Normalize azimuth to [0, 360) range"""
        if self.unit == "deg":
            self.nominal_value = self.nominal_value % 360
        elif self.unit == "rad":
            self.nominal_value = self.nominal_value % (2 * math.pi)
        elif self.unit == "grad":
            self.nominal_value = self.nominal_value % 400

    def to_bearing(self) -> str:
        """Convert azimuth to bearing notation (N45°E format)"""
        deg = self.to_unit("deg")
        if deg <= 90:
            return f"N{deg:.1f}°E"
        elif deg <= 180:
            return f"S{180-deg:.1f}°E"
        elif deg <= 270:
            return f"S{deg-180:.1f}°W"
        else:
            return f"N{360-deg:.1f}°W"

    def to_quadrant(self) -> str:
        """Get the quadrant (NE, SE, SW, NW)"""
        deg = self.to_unit("deg")
        if deg <= 90:
            return "NE"
        elif deg <= 180:
            return "SE"
        elif deg <= 270:
            return "SW"
        else:
            return "NW"

class Area(Quantity):
    """Represents area measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "ft2": 1,  # Base unit
            "acre": 2.30E-05,
            "cm2": 929.0304,
            "ha": 9.29E-06,
            "in2": 144,
            "km2": 9.29E-08,
            "m2": 0.9290304,
            "mi2": 3.59E-08,
            "mm2": 92903.04,
        }

    @property
    def valid_range(self) -> Tuple[Optional[float], Optional[float]]:
        """Area must be positive"""
        return (0, None)

    def calculate_diameter(self) -> 'Diameter':
        """Calculate diameter assuming circular area"""
        area_ft2 = self.to_unit("ft2")
        diameter_ft = 2 * math.sqrt(area_ft2 / math.pi)
        return Diameter(diameter_ft, "ft", self.uncertainty)

class Weight(Quantity):
    """Represents weight measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "lbf": 1,  # Base unit
            "kg": 0.45359237,
            "N": 4.448221615,
            "kN": 0.004448222,
            "tonf": 0.0005,
            "kgf": 0.45359237
        }

    @property
    def valid_range(self) -> Tuple[Optional[float], Optional[float]]:
        """Weight must be positive"""
        return (0, None)

    def calculate_mass(self, g: float = 9.81) -> 'Mass':
        """Calculate mass given local gravitational acceleration"""
        force_n = self.to_unit("N")
        mass_kg = force_n / g
        return Mass(mass_kg, "kg", self.uncertainty)

class LinearDensity(Quantity):
    """Represents linear density (weight per unit length)"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "kg/m": 1,  # Base unit
            "lb/ft": 1.488164,
            "N/m": 9.80665
        }

    @property
    def valid_range(self) -> Tuple[Optional[float], Optional[float]]:
        """Linear density must be positive"""
        return (0, None)

    def calculate_weight(self, length: 'Length') -> 'Weight':
        """Calculate total weight for a given length"""
        base_density = self.to_unit("kg/m")
        length_m = length.to_unit("m")
        total_weight_kg = base_density * length_m
        return Weight(total_weight_kg, "kg", 
                     math.sqrt((self.uncertainty * length_m)**2 + 
                             (base_density * length.uncertainty)**2) if self.uncertainty else None)

class Pressure(Quantity):
    """Represents pressure measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "psi": 1,  # Base unit
            "atm": 0.068045964,
            "bar": 0.068947573,
            "bara": 0.068947573,
            "barg": 0.068947573,
            "cmH2O": 70.30695796,
            "gf/cm2": 70.30695796,
            "GPa": 6.89E-06,
            "kgf/cm2": 0.070306958,
            "kPa": 6.894757293,
            "MPa": 0.006894757,
            "Pa": 6894.757293,
            "psig": 1.0
        }

    def calculate_hydrostatic_pressure(self, fluid_density: 'Density', depth: 'Depth') -> 'Pressure':
        """Calculate hydrostatic pressure given fluid density and depth"""
        density_kg_m3 = fluid_density.to_unit("kg/m3")
        depth_m = depth.to_unit("m")
        pressure_pa = density_kg_m3 * 9.81 * depth_m
        return Pressure(pressure_pa, "Pa", 
                       math.sqrt((9.81 * depth_m * fluid_density.uncertainty)**2 + 
                               (9.81 * density_kg_m3 * depth.uncertainty)**2) if self.uncertainty else None)

    def calculate_equivalent_mud_weight(self, depth: 'Depth') -> 'Density':
        """Calculate equivalent mud weight (EMW) from pressure and depth"""
        pressure_psi = self.to_unit("psi")
        depth_ft = depth.to_unit("ft")
        emw = pressure_psi / (0.052 * depth_ft)  # 0.052 is the pressure gradient constant
        return Density(emw, "ppg", self.uncertainty)

class Torque(Quantity):
    """Represents torque measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "klbf.ft": 1,  # Base unit
            "J": 1355.817948,
            "kN.m": 1.355817948,
            "lbf.ft": 1000,
            "N.m": 1355.817948,
            "daN.m": 135.5817948,
            "kdaN.m": 0.135581795
        }

    def calculate_power(self, angular_velocity: float) -> 'Energy':
        """Calculate power given angular velocity (rpm)"""
        torque_nm = self.to_unit("N.m")
        # Convert rpm to rad/s
        angular_velocity_rad_s = angular_velocity * 2 * math.pi / 60
        power_watts = torque_nm * angular_velocity_rad_s
        return Energy(power_watts, "J", self.uncertainty)

class BarrelOfOilEquivalent(Quantity):
    """Represents barrel of oil equivalent measurements"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "boe": 1,  # Base unit
            "Mboe": 0.001,
            "MMboe": 1.00E-06,
            "scf": 5800,  # Approximate conversion for natural gas
            "Mscf": 5.8
        }

    def to_gas_volume(self) -> 'Volume':
        """Convert BOE to standard cubic feet of gas"""
        gas_scf = self.to_unit("scf")
        return Volume(gas_scf, "scf", self.uncertainty)

class DLS(Quantity):
    """Represents Dogleg Severity measurements"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "deg/100ft": 1,  # Base unit
            "deg/100m": 3.280839895,
            "deg/10m": 0.32808399,
            "deg/30ft": 0.3,
            "deg/30m": 0.984251969,
            "deg/ft": 0.01,
            "deg/m": 0.032808339,
            "rad/ft": 0.000174533,
            "rad/m": 0.000572615
        }

    def calculate_radius_of_curvature(self) -> 'Length':
        """Calculate radius of curvature from DLS"""
        dls_deg_100ft = self.to_unit("deg/100ft")
        if dls_deg_100ft == 0:
            return Length(float('inf'), "ft")
        radius_ft = 100 / (2 * math.sin(math.radians(dls_deg_100ft/2)))
        return Length(radius_ft, "ft", self.uncertainty)

class Density(Quantity):
    """Represents density measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "lb/gal": 1,  # Base unit (ppg)
            "g/cm3": 0.119826427,
            "kg/m3": 119.8264273,
            "kg/l": 0.119826427,
            "lb/ft3": 7.480519481,
            "SG": 0.119826427,  # Specific Gravity
            "lb/bbl": 42
        }

    def calculate_hydrostatic_gradient(self) -> float:
        """Calculate hydrostatic pressure gradient in psi/ft"""
        ppg = self.to_unit("lb/gal")
        return ppg * 0.052  # Pressure gradient constant

    def calculate_pressure_at_depth(self, depth: 'Depth') -> 'Pressure':
        """Calculate hydrostatic pressure at given depth"""
        gradient = self.calculate_hydrostatic_gradient()
        depth_ft = depth.to_unit("ft")
        pressure = gradient * depth_ft
        return Pressure(pressure, "psi", 
                       math.sqrt((depth_ft * self.uncertainty * 0.052)**2 + 
                               (gradient * depth.uncertainty)**2) if self.uncertainty else None)

class Energy(Quantity):
    """Represents energy measurements"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "J": 1,  # Base unit
            "kJ": 0.001,
            "MJ": 1e-6,
            "kWh": 2.777778e-7,
            "Btu": 0.000947817,
            "ft.lbf": 0.737562149,
            "kcal": 0.000239006
        }

    def calculate_power(self, time_seconds: float) -> float:
        """Calculate power in watts given time in seconds"""
        joules = self.to_unit("J")
        return joules / time_seconds

class FluidPressure(Pressure):
    """Specialized pressure class for fluid systems"""
    
    def calculate_flow_coefficient(self, flow_rate: 'FlowRate', density: 'Density') -> float:
        """Calculate flow coefficient (Cv)"""
        delta_p_psi = self.to_unit("psi")
        flow_gpm = flow_rate.to_unit("gal/min")
        sg = density.to_unit("SG")
        return flow_gpm * math.sqrt(sg / delta_p_psi)

    def calculate_equivalent_circulating_density(self, static_density: 'Density', 
                                              annular_pressure_loss: 'Pressure', 
                                              true_vertical_depth: 'Depth') -> 'Density':
        """Calculate Equivalent Circulating Density (ECD)"""
        tvd_ft = true_vertical_depth.to_unit("ft")
        static_ppg = static_density.to_unit("lb/gal")
        apl_psi = annular_pressure_loss.to_unit("psi")
        
        ecd = static_ppg + (apl_psi / (0.052 * tvd_ft))
        return Density(ecd, "lb/gal", 
                      math.sqrt(static_density.uncertainty**2 + 
                              (annular_pressure_loss.uncertainty / (0.052 * tvd_ft))**2) if self.uncertainty else None)
        
class FluidVolume(Quantity):
    """Represents fluid volume measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "bbl": 1,  # Base unit
            "Bcf": 5.61E-09,
            "ft3": 5.614583333,
            "m3": 0.158987,
            "Mbbl": 0.001,
            "MMbbl": 1.00E-06,
            "MMScf": 5.614583333,
            "Tscf": 5.61E-12
        }

    @property
    def valid_range(self) -> Tuple[Optional[float], Optional[float]]:
        """Volume must be positive"""
        return (0, None)

    def calculate_height_in_annulus(self, wellbore_diameter: 'Diameter', 
                                  pipe_diameter: 'Diameter') -> 'Length':
        """Calculate fluid height in annular space"""
        wellbore_area = math.pi * (wellbore_diameter.to_unit("in")**2 - 
                                 pipe_diameter.to_unit("in")**2) / 4
        volume_cuft = self.to_unit("ft3")
        height_ft = volume_cuft / (wellbore_area / 144)  # Convert sq inches to sq ft
        return Length(height_ft, "ft", self.uncertainty)

    def calculate_capacity(self, length: 'Length') -> 'UnitCapacity':
        """Calculate volume per unit length"""
        volume_bbl = self.to_unit("bbl")
        length_ft = length.to_unit("ft")
        capacity = volume_bbl / length_ft
        return UnitCapacity(capacity, "bbl/ft", 
                           math.sqrt((self.uncertainty/length_ft)**2 + 
                                   (volume_bbl*length.uncertainty/length_ft**2)**2) if self.uncertainty else None)

class Force(Quantity):
    """Represents force measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "klbf": 1,  # Base unit
            "daN": 444.8221615,
            "dyn": 444822161.5,
            "gf": 453539.237,
            "kN": 4.448221615,
            "lbf": 1000,
            "N": 4448.221615,
            "tonf": 0.45359237
        }

    def calculate_pressure(self, area: 'Area') -> 'Pressure':
        """Calculate pressure given an area"""
        force_lbf = self.to_unit("lbf")
        area_sqin = area.to_unit("in2")
        pressure = force_lbf / area_sqin
        return Pressure(pressure, "psi", 
                       math.sqrt((self.uncertainty/area_sqin)**2 + 
                               (force_lbf*area.uncertainty/area_sqin**2)**2) if self.uncertainty else None)

class Mass(Quantity):
    """Represents mass measurements"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "kg": 1,  # Base unit
            "g": 1000,
            "lb": 2.20462,
            "klb": 0.00220462,
            "ton": 0.001,
            "Ukton": 0.000984207,
            "Uston": 0.00110231
        }

    def calculate_weight(self, g: float = 9.81) -> 'Weight':
        """Calculate weight force given gravitational acceleration"""
        mass_kg = self.to_unit("kg")
        weight_n = mass_kg * g
        return Weight(weight_n, "N", self.uncertainty * g if self.uncertainty else None)

class MudWeight(Density):
    """Specialized density class for drilling fluids"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "lb/gal": 1,  # Base unit (ppg)
            "kg/m3": 119.8264273,
            "kg/L": 0.119826427,
            "sg": 0.119826427,
            "psi/1000ft": 0.051948052  # Pressure gradient
        }

    def calculate_hydrostatic_pressure_gradient(self) -> float:
        """Calculate pressure gradient in psi/ft"""
        ppg = self.to_unit("lb/gal")
        return ppg * 0.052

    def calculate_ecd(self, annular_pressure_loss: 'Pressure', 
                     true_vertical_depth: 'Depth') -> 'MudWeight':
        """Calculate Equivalent Circulating Density"""
        static_ppg = self.to_unit("lb/gal")
        apl_psi = annular_pressure_loss.to_unit("psi")
        tvd_ft = true_vertical_depth.to_unit("ft")
        
        ecd = static_ppg + (apl_psi / (0.052 * tvd_ft))
        return MudWeight(ecd, "lb/gal", self.uncertainty)

class PumpPressure(Pressure):
    """Specialized pressure class for pump operations"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "psi": 1,  # Base unit
            "bar": 0.068947573,
            "kPa": 6.894757293,
            "MPa": 0.006894757,
            "Pa": 6894.757293
        }

    def calculate_hydraulic_horsepower(self, flow_rate: 'FlowRate') -> float:
        """Calculate hydraulic horsepower"""
        pressure_psi = self.to_unit("psi")
        flow_gpm = flow_rate.to_unit("gal/min")
        return pressure_psi * flow_gpm / 1714  # 1714 is the hydraulic horsepower constant

class SaltConcentration(Quantity):
    """Represents salt concentration in drilling fluids"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "lb/bbl": 1,  # Base unit
            "g/L": 2.853010174,
            "kg/m3": 2.853010174,
            "ppm": 2853.010174
        }

    def calculate_chloride_concentration(self) -> float:
        """Calculate chloride ion concentration assuming NaCl"""
        nacl_ppb = self.to_unit("lb/bbl")
        return nacl_ppb * 0.6  # Chloride proportion in NaCl

class Stress(Quantity):
    """Represents stress measurements"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "psi": 1,  # Base unit
            "Pa": 6894.757293,
            "kPa": 6.894757293,
            "MPa": 0.006894757,
            "ksi": 0.001,
            "bar": 0.068947573
        }

    def calculate_strain(self, youngs_modulus: 'Stress') -> float:
        """Calculate strain using Hooke's law"""
        stress = self.to_unit("psi")
        modulus = youngs_modulus.to_unit("psi")
        return stress / modulus

class Viscosity(Quantity):
    """Represents viscosity measurements"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "cp": 1,  # Base unit (centipoise)
            "Pa.s": 0.001,
            "mPa.s": 1,
            "lb/ft.s": 0.000671969,
            "poise": 0.01
        }

    def calculate_reynolds_number(self, velocity: 'Velocity', 
                                diameter: 'Diameter', 
                                density: 'Density') -> float:
        """Calculate Reynolds number"""
        visc_pas = self.to_unit("Pa.s")
        vel_ms = velocity.to_unit("m/s")
        dia_m = diameter.to_unit("m")
        dens_kgm3 = density.to_unit("kg/m3")
        
        return (dens_kgm3 * vel_ms * dia_m) / visc_pas

class UnitCapacity(Quantity):
    """Represents volume per unit length"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "bbl/ft": 1,  # Base unit
            "ft3/ft": 5.614575335,
            "m3/m": 0.521610892,
            "gal/ft": 42.00002354,
            "L/m": 521.6108924
        }

    def calculate_volume(self, length: 'Length') -> 'FluidVolume':
        """Calculate total volume for a given length"""
        capacity_bblft = self.to_unit("bbl/ft")
        length_ft = length.to_unit("ft")
        volume = capacity_bblft * length_ft
        return FluidVolume(volume, "bbl", 
                          math.sqrt((length_ft*self.uncertainty)**2 + 
                                  (capacity_bblft*length.uncertainty)**2) if self.uncertainty else None)

class FlowRate(Quantity):
    """Represents flow rate measurements"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "gpm": 1,  # Base unit (gallons per minute)
            "bbl/day": 34.285714,
            "m3/day": 5.450992969,
            "L/min": 3.785411784,
            "ft3/min": 0.133680556,
            "m3/hr": 0.227124707
        }

    def calculate_velocity(self, diameter: 'Diameter') -> 'Velocity':
        """Calculate fluid velocity in pipe"""
        flow_gpm = self.to_unit("gpm")
        dia_inch = diameter.to_unit("in")
        
        velocity_ftmin = (flow_gpm * 0.321) / (dia_inch ** 2)
        return Velocity(velocity_ftmin, "ft/min", self.uncertainty)

    def calculate_reynolds_number(self, diameter: 'Diameter', 
                                viscosity: 'Viscosity', 
                                density: 'Density') -> float:
        """Calculate Reynolds number"""
        flow_m3s = self.to_unit("m3/day") / 86400  # Convert to m3/s
        dia_m = diameter.to_unit("m")
        visc_pas = viscosity.to_unit("Pa.s")
        dens_kgm3 = density.to_unit("kg/m3")
        
        velocity = (4 * flow_m3s) / (math.pi * dia_m**2)
        return (dens_kgm3 * velocity * dia_m) / visc_pas

class WeightOnBit(Force):
    """Represents weight on bit measurements"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "klbf": 1,  # Base unit (1000 pounds force)
            "tonf": 0.45359237,
            "kN": 4.448221615,
            "daN": 444.8221615,
            "N": 4448.221615
        }

    def calculate_pressure_on_bit(self, bit_diameter: 'Diameter') -> 'Pressure':
        """Calculate pressure on bit face"""
        force_lbf = self.to_unit("lbf")
        area_sqin = math.pi * (bit_diameter.to_unit("in")/2)**2
        pressure = force_lbf / area_sqin
        return Pressure(pressure, "psi", self.uncertainty)

class WeightPerLength(LinearDensity):
    """Represents weight per unit length"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "lb/ft": 1,  # Base unit
            "kg/m": 1.488164,
            "N/m": 14.59390292,
            "lbf/in": 12
        }

    def calculate_buoyed_weight(self, fluid_density: 'Density') -> 'WeightPerLength':
        """Calculate buoyed weight in fluid"""
        weight_lbft = self.to_unit("lb/ft")
        fluid_ppg = fluid_density.to_unit("lb/gal")
        
        # Buoyancy factor calculation
        buoyancy_factor = 1 - (fluid_ppg / 65.5)  # 65.5 ppg is steel density
        buoyed_weight = weight_lbft * buoyancy_factor
        
        return WeightPerLength(buoyed_weight, "lb/ft", self.uncertainty * buoyancy_factor)

class WeightPerLength(Quantity):
    """Represents temperature measurements"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "degF": 1,  # Base unit
            "degC": 1,  # Special handling required
            "K": 1,     # Special handling required
            "degR": 459.67  # Rankine offset
        }

    def to_unit(self, target_unit: str) -> float:
        """Override to_unit for special temperature conversion handling"""
        if not self._is_valid_unit(target_unit):
            raise ValueError(f"Invalid target unit '{target_unit}'")
            
        if self.unit == target_unit:
            return self.value
            
        # Convert to Fahrenheit first
        if self.unit == "degC":
            fahrenheit = (self.value * 9/5) + 32
        elif self.unit == "K":
            fahrenheit = (self.value - 273.15) * 9/5 + 32
        elif self.unit == "degR":
            fahrenheit = self.value - 459.67
        else:
            fahrenheit = self.value
            
        # Convert from Fahrenheit to target
        if target_unit == "degC":
            return (fahrenheit - 32) * 5/9
        elif target_unit == "K":
            return (fahrenheit - 32) * 5/9 + 273.15
        elif target_unit == "degR":
            return fahrenheit + 459.67
        else:
            return fahrenheit

    def calculate_thermal_expansion(self, length: 'Length', 
                                  coefficient: float) -> 'Length':
        """Calculate thermal expansion of material"""
        delta_t = self.to_unit("degF") - 68  # Reference temperature 68°F
        original_length = length.to_unit("ft")
        expansion = original_length * (1 + coefficient * delta_t)
        return Length(expansion, "ft", 
                     math.sqrt((length.uncertainty * (1 + coefficient * delta_t))**2 + 
                             (original_length * coefficient * self.uncertainty)**2) if self.uncertainty else None)

class Velocity(Quantity):
    """Represents velocity measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "ft/min": 1,  # Base unit
            "cm/day": 43891.2,
            "cm/h": 1828.8,
            "cm/ms": 0.000508,
            "cm/s": 0.508,
            "cm/yr": 16031260.8,
            "d/ft eq.": 0.000694444,
            "d/km eq.": 2.278361038,
            "d/m eq.": 0.002278361,
            "ft/d": 1440,
            "ft/hr": 60,
            "ft/ms": 1.67E-05,
            "ft/s": 0.016666667,
            "ft/yr": 525960,
            "km/h": 0.018288,
            "km/s": 5.08E-06,
            "m/d": 438.912,
            "m/hr": 18.288,
            "m/min": 0.3048,
            "m/ms": 5.08E-06,
            "m/s": 0.00508,
            "m/yr": 160312.608,
            "mi/hr": 0.011363636
        }

    @property
    def valid_range(self) -> Tuple[Optional[float], Optional[float]]:
        """Velocity can be positive or negative"""
        return (None, None)

    def calculate_reynolds_number(self, diameter: 'Diameter', 
                                density: 'Density', 
                                viscosity: 'Viscosity') -> float:
        """Calculate Reynolds number
        
        Args:
            diameter: Characteristic length (pipe diameter)
            density: Fluid density
            viscosity: Fluid viscosity
            
        Returns:
            Reynolds number (dimensionless)
        """
        velocity_ms = self.to_unit("m/s")
        diameter_m = diameter.to_unit("m")
        density_kgm3 = density.to_unit("kg/m3")
        viscosity_pas = viscosity.to_unit("Pa.s")
        
        reynolds = (density_kgm3 * abs(velocity_ms) * diameter_m) / viscosity_pas
        
        # Calculate uncertainty if available
        if any([self.uncertainty, diameter.uncertainty, 
               density.uncertainty, viscosity.uncertainty]):
            rel_uncertainty = math.sqrt(
                (self.uncertainty/velocity_ms if self.uncertainty else 0)**2 +
                (diameter.uncertainty/diameter_m if diameter.uncertainty else 0)**2 +
                (density.uncertainty/density_kgm3 if density.uncertainty else 0)**2 +
                (viscosity.uncertainty/viscosity_pas if viscosity.uncertainty else 0)**2
            )
            return ufloat(reynolds, reynolds * rel_uncertainty)
        
        return reynolds

    def calculate_friction_factor(self, diameter: 'Diameter', 
                                roughness: 'Length', 
                                density: 'Density', 
                                viscosity: 'Viscosity') -> float:
        """Calculate Darcy friction factor using Colebrook-White equation
        
        Args:
            diameter: Pipe diameter
            roughness: Pipe roughness
            density: Fluid density
            viscosity: Fluid viscosity
            
        Returns:
            Darcy friction factor (dimensionless)
        """
        reynolds = self.calculate_reynolds_number(diameter, density, viscosity)
        if isinstance(reynolds, uncertainties.UFloat):
            reynolds = reynolds.nominal_value
            
        if reynolds < 2300:
            # Laminar flow
            return 64 / reynolds
        
        # Turbulent flow - iterative solution
        relative_roughness = roughness.to_unit("m") / diameter.to_unit("m")
        
        def colebrook(f):
            return 1/math.sqrt(f) + 2 * math.log10(relative_roughness/3.7 + 2.51/(reynolds*math.sqrt(f)))
        
        # Initial guess using Swamee-Jain equation
        f = 0.25 / (math.log10(relative_roughness/3.7 + 5.74/reynolds**0.9))**2
        
        # Newton-Raphson iteration
        for _ in range(20):
            f_new = f - colebrook(f)/((-1/(2*f**1.5)) - 
                                    2.51/(reynolds*f*math.log(10)*(relative_roughness/3.7 + 
                                                                  2.51/(reynolds*math.sqrt(f)))))
            if abs(f_new - f) < 1e-6:
                return f_new
            f = f_new
        
        return f

    def calculate_pressure_loss(self, length: 'Length', 
                              diameter: 'Diameter',
                              density: 'Density',
                              roughness: 'Length',
                              viscosity: 'Viscosity') -> 'Pressure':
        """Calculate pressure loss due to friction
        
        Args:
            length: Pipe length
            diameter: Pipe diameter
            density: Fluid density
            roughness: Pipe roughness
            viscosity: Fluid viscosity
            
        Returns:
            Pressure loss
        """
        f = self.calculate_friction_factor(diameter, roughness, density, viscosity)
        velocity_ms = self.to_unit("m/s")
        length_m = length.to_unit("m")
        diameter_m = diameter.to_unit("m")
        density_kgm3 = density.to_unit("kg/m3")
        
        pressure_loss_pa = (f * length_m * density_kgm3 * velocity_ms**2) / (2 * diameter_m)
        
        return Pressure(pressure_loss_pa, "Pa", 
                       pressure_loss_pa * math.sqrt(
                           (self.uncertainty/velocity_ms if self.uncertainty else 0)**2 +
                           (length.uncertainty/length_m if length.uncertainty else 0)**2 +
                           (diameter.uncertainty/diameter_m if diameter.uncertainty else 0)**2 +
                           (density.uncertainty/density_kgm3 if density.uncertainty else 0)**2
                       ) if any([self.uncertainty, length.uncertainty, 
                               diameter.uncertainty, density.uncertainty]) else None)

    def calculate_displacement_time(self, distance: 'Length') -> float:
        """Calculate time required to travel a distance
        
        Args:
            distance: Distance to travel
            
        Returns:
            Time in minutes
        """
        velocity_ftmin = self.to_unit("ft/min")
        distance_ft = distance.to_unit("ft")
        
        return distance_ft / velocity_ftmin

class Volume(Quantity):
    """Represents volume measurements in well engineering"""
    
    @property
    def conversion_factors(self) -> Dict[str, float]:
        return {
            "ft3": 1,  # Base unit
            "acre.ft": 0.000022957,
            "bbl": 0.178107607,
            "Bcf": 1E-09,
            "cm3": 28316.846592,
            "Gm3": 2.83168E-11,
            "galUK": 6.228835459,
            "galUS": 7.480519481,
            "km3": 2.83168E-11,
            "L": 28.316846592,
            "m3": 0.028316847,
            "Mbbl": 0.000178108,
            "Mcf": 0.001,
            "MgalUK": 0.006228835,
            "MgalUS": 0.007480519,
            "MMbbl": 1.78108E-07,
            "MMcf": 1E-06,
            "MMgalUK": 6.22884E-06,
            "MMgalUS": 7.48052E-06,
            "rb": 0.178107607,
            "scf": 1
        }

    @property
    def valid_range(self) -> Tuple[Optional[float], Optional[float]]:
        """Volume must be positive"""
        return (0, None)

    def calculate_height_in_tank(self, area: 'Area') -> 'Length':
        """Calculate fluid height in a tank of given cross-sectional area
        
        Args:
            area: Tank cross-sectional area
            
        Returns:
            Fluid height
        """
        volume_ft3 = self.to_unit("ft3")
        area_ft2 = area.to_unit("ft2")
        
        height = volume_ft3 / area_ft2
        return Length(height, "ft", 
                     math.sqrt((self.uncertainty/area_ft2 if self.uncertainty else 0)**2 +
                             (volume_ft3*area.uncertainty/area_ft2**2 if area.uncertainty else 0)**2))

    def calculate_displacement(self, density: 'Density') -> 'Weight':
        """Calculate buoyant force when submerged in fluid
        
        Args:
            density: Fluid density
            
        Returns:
            Buoyant force
        """
        volume_m3 = self.to_unit("m3")
        density_kgm3 = density.to_unit("kg/m3")
        
        force_n = volume_m3 * density_kgm3 * 9.81
        return Weight(force_n, "N", 
                     force_n * math.sqrt(
                         (self.uncertainty/volume_m3 if self.uncertainty else 0)**2 +
                         (density.uncertainty/density_kgm3 if density.uncertainty else 0)**2
                     ) if any([self.uncertainty, density.uncertainty]) else None)

    def calculate_capacity_factor(self, nominal_volume: 'Volume') -> float:
        """Calculate capacity factor (actual/nominal volume ratio)
        
        Args:
            nominal_volume: Nominal or design volume
            
        Returns:
            Capacity factor (dimensionless)
        """
        actual = self.to_unit("ft3")
        nominal = nominal_volume.to_unit("ft3")
        
        return actual / nominal

    def calculate_residence_time(self, flow_rate: 'FlowRate') -> float:
        """Calculate fluid residence time
        
        Args:
            flow_rate: Volumetric flow rate
            
        Returns:
            Residence time in minutes
        """
        volume_ft3 = self.to_unit("ft3")
        flow_ft3min = flow_rate.to_unit("ft3/min")
        
        return volume_ft3 / flow_ft3min

    @classmethod
    def from_dimensions(cls, length: 'Length', width: 'Length', 
                       height: 'Length') -> 'Volume':
        """Create volume from rectangular dimensions
        
        Args:
            length: Length
            width: Width
            height: Height
            
        Returns:
            Volume object
        """
        # Convert all to same unit
        l = length.to_unit("ft")
        w = width.to_unit("ft")
        h = height.to_unit("ft")
        
        volume = l * w * h
        
        # Calculate uncertainty if available
        if any([length.uncertainty, width.uncertainty, height.uncertainty]):
            rel_uncertainty = math.sqrt(
                (length.uncertainty/l if length.uncertainty else 0)**2 +
                (width.uncertainty/w if width.uncertainty else 0)**2 +
                (height.uncertainty/h if height.uncertainty else 0)**2
            )
            return cls(volume, "ft3", volume * rel_uncertainty)
        
        return cls(volume, "ft3")

    @classmethod
    def from_cylinder(cls, diameter: 'Diameter', length: 'Length') -> 'Volume':
        """Create volume from cylindrical dimensions
        
        Args:
            diameter: Cylinder diameter
            length: Cylinder length
            
        Returns:
            Volume object
        """
        radius_ft = diameter.to_unit("ft") / 2
        length_ft = length.to_unit("ft")
        
        volume = math.pi * radius_ft**2 * length_ft
        
        # Calculate uncertainty if available
        if any([diameter.uncertainty, length.uncertainty]):
            rel_uncertainty = math.sqrt(
                (2 * diameter.uncertainty/diameter.to_unit("ft") if diameter.uncertainty else 0)**2 +
                (length.uncertainty/length_ft if length.uncertainty else 0)**2
            )
            return cls(volume, "ft3", volume * rel_uncertainty)
        
        return cls(volume, "ft3")
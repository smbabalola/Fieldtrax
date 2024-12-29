import math;

class Quantity:
    """A base class for all units."""
    def __init__(self, value, quantity):
        self.value = value
        self.quantity = quantity
        self.conversion_factors = {}  # Empty conversion factors dictionary

    def __repr__  (self):
        return f"{self.value} {self.quantity}"
    
    def __round__(self, ndigits=None):
        """Rounds the value to the specified number of decimal places."""
        if ndigits is None:
            ndigits = 2
        return round(self.value, ndigits)
    
    # def to_inches(self):
    #     """Converts the wellbore diameter to inches."""
    #     return self.value * self.conversion_factors[self.quantity]

    # def to_unit(self, quantity):
    #     inches = self.to_inches()
    #     return inches / self.conversion_factors[quantity]
        
    def to_unit(self, quantity):
        if self.value == 0:
            return 0
        if self.quantity == quantity:
            return self.value  # No conversion needed
        elif self.conversion_factors[quantity] == 1:
                converted_value = self.value/self.conversion_factors[self.quantity]
                return converted_value
            # conversion_factor = self.conversion_factors[from_unit][to_unit]
        converted_value = (self.value * self.conversion_factors[quantity]/self.conversion_factors[self.quantity])
        return converted_value
    
    def convert_to_all_units(self, precision = 4):
        """Converts the value to all available units.

        Returns:
            list: A list of tuples containing the converted value and unit.
        """
        results = []
        for unit in self.conversion_factors.keys():
            converted_value = round(self.to_unit(unit),precision)
            print(converted_value, unit)
            results.append((round(converted_value,precision), unit))
        return results
    
    def format(self, unit, precision=2, rounding_mode="ROUND_HALF_UP"):
        """Formats the wellbore diameter to a specified unit with precision."""
        formatted_value = self.to_unit(unit)  # Assuming it returns a float
        rounded_value = round(formatted_value, precision)
        return f"{rounded_value:.{precision}f} {self.quantity}"

    def to_default_quantity(self):
        """Converts the value to the default quantity (if defined).

        Returns:
            Quantity: The value in the default quantity.
        """
        # Implement logic to determine the default quantity and convert
        # (e.g., if a default unit is defined, use it)
        print("self value: ", self.value,"/ conversion factor: ",self.conversion_factors[self.quantity])
        return self.value / self.conversion_factors[self.quantity]
    
    def __add__(self, other):
        if self.quantity != other.quantity:
            raise ValueError("Cannot add values with different units")
        return Quantity(self.value + other.value, self.quantity)

    def __sub__(self, other):
        """Subtracts two quantities"""
        if self.quantity != other.quantity:
            raise ValueError("Cannot subtract quantities with different units")
        return Quantity(self.value - other.value, self.quantity)

    def __mul__(self, other):
        """Multiplies a Quantity by a scalar."""
        return Quantity(self.value * other, self.quantity)

    def __truediv__(self, other):
        """Divides a Quantity by a scalar."""
        return Quantity(self.value / other, self.quantity)

    def __eq__(self, other):
        """Compares two Quantity."""
        if self.quantity != other.quantity:
            return False
        return self.value == other.value

    def __gt__(self, other):
        """Subtracts two quantities"""
        if self.quantity != other.quantity:
            raise ValueError("Cannot subtract quantities with different units")
        if self.value > other.value:
            return True
            
class Depth(Quantity):
    def __init__(self, value, quantity):
        super().__init__(value, quantity)
        self.conversion_factors = {
        "ft": 1,
        "ftSe":	1.000017338,
        "cm": 30.48,
        "ftUS":	0.999998,
        "in": 12,
        "m": 0.3048,
        "mm": 304.8,
        "km": 0.0003048,
        "mi": 0.000189394,
        "yd":0.333333333,
        }

class Length(Depth):
    def __init__(self, value, quantity):
        super().__init__(value, quantity)
        
class Diameter(Quantity):
    def __init__(self, value, quantity):
        super().__init__(value, quantity)
        self.conversion_factors = {
        "in": 1,
        "cm": 2.54,
        "ft": 0.0833333333,
        "m": 0.0254,
        "mm":	25.4
        # Add more units and conversion factors as needed
    }

class Azimuth(Quantity):
    conversion_factors = {
        "deg": 1,
        "rad": math.pi / 180,
        "grads": 0.9 * math.pi / 180
    }

    def __init__(self, value, unit):
        super().__init__(value, unit)

        # Ensure azimuth is within the valid range (0 to 360 degrees)
        if self.unit == "deg" and not (0 <= self.value <= 360):
            raise ValueError("Azimuth must be between 0 and 360 degrees")

    # ... other methods from the Unit class ...

    def normalize(self):
        """Normalizes the azimuth to the range 0 to 360 degrees."""
        while self.value < 0:
            self.value += 360
        while self.value > 360:
            self.value -= 360

    def to_degrees(self):
        return self.to_unit("degrees")

    def to_radians(self):
        return self.to_unit("radians")

    def to_grads(self):
        return self.to_unit("grads")

class Area(Quantity):
    def __init__(self, value, quantity):
        super().__init__(value, quantity)
        self.conversion_factors = {
        "ft2": 1,
        "acre":	2.30E-05,
        "cm2": 929.0304,
        "ha": 9.29E-06,
        "in2": 144,
        "km2": 9.29E-08,
        "m2": 0.9290304,
        "mi2": 3.59E-08,
        "mm2": 92903.04,
        }   
                
class Weight(Quantity):
    """Represents a weight quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the weight.
        quantity (str): The unit of measurement for the weight.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to kilograms.
    """

    def __init__(self, value, quantity):
        """Initializes a Weight object.

        Args:
            value (float): The numerical value of the weight.
            quantity (str): The unit of measurement for the weight.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
            "kg": 1,
            "lbs": 0.45359237,
            "N": 0.101971621
        }
        
class LinearDensity(Quantity):
    """Represents a linear density quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the linear density.
        quantity (str): The unit of measurement for the linear density.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to kilograms per meter.
    """

    def __init__(self, value, quantity):
        """Initializes a LinearDensity object.

        Args:
            value (float): The numerical value of the linear density.
            quantity (str): The unit of measurement for the linear density.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
            "kg/m": 1,
            "lb/ft": 1.488164,
            "N/m": 0.101971621
        }
        
class Pressure(Quantity):
    """Represents a pressure quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Pressure object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
            "Psi":	1,
            "atm":	0.068045964,
            "bar":	0.068947573,
            "bara":	0.068947573,
            "barg":	0.068947573,
            "cmH2O":	70.30695796,
            "gf/100cm2":	7030.695796,
            "GPa":	6.89E-06,
            "kgf/cm2":	0.070306958,
            "kgf/m2":	703.0695796,
            "kN/m2":	6.894757293,
            "kPa":	6.894757293,
            "kpsi":	0.001,
            "lbf/100ft2":	14400,
            "mbar":	68.94757293,
            "mmHg":	51.7149252,
            "mPa":	0.006894757,
            "N/m2":	6894.757293,
            "N/mm2":	0.006894757,
            "Psf":	144, 
            "psia":	1,
            "psig":	14.69594878,
            "Torr":	51.71493226,
        }

class Torque(Quantity):
    """Represents a torque quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the torque.
        quantity (str): The unit of measurement for the torque.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to newton-meters.
    """

    def __init__(self, value, quantity):
        """Initializes a Torque object.

        Args:
            value (float): The numerical value of the torque.
            quantity (str): The unit of measurement for the torque.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
            "klbf.ft":	1,
            "J":	1355.817948,
            "kN.m":	1.355817948,
            "lbf.ft":	1000,
            "N.m":	1355.817948,
            "daN.m":	135.5817948,
            "kdaN.m":	0.135581795,
        }
    # ... rest of the class remains the same as in the previous responses 
        
class BarrelofOilEquivalent(Quantity):
    """Represents a barrel of oil equivalent quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the capacity.
        quantity (str): The unit of measurement for the capacity.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to barrels per foot.
    """

    def __init__(self, value, quantity):
        """Initializes a Barrel of Oil Equivalent object.

        Args:
            value (float): The numerical value of the capacity.
            quantity (str): The unit of measurement for the capacity.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "boe":	1,
        "Mboe":	0.001,
        "Mmboe":	1.00E-06
        }        
        
class BitNozzleDiameter(Quantity):
    """Represents a bit nozzle diameter quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the capacity.
        quantity (str): The unit of measurement for the capacity.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to barrels per foot.
    """

    def __init__(self, value, quantity):
        """Initializes a Bit nozzle diameter object.

        Args:
            value (float): The numerical value of the capacity.
            quantity (str): The unit of measurement for the capacity.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "in":	1,
        "in/32": 32,
        "m": 0.0254,
        "mm": 25.4
        }
        
class DLS(Quantity):
    """Represents a dogleg severity quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the capacity.
        quantity (str): The unit of measurement for the capacity.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to barrels per foot.
    """

    def __init__(self, value, quantity):
        """Initializes a Dog leg severity object.

        Args:
            value (float): The numerical value of the capacity.
            quantity (str): The unit of measurement for the capacity.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "deg/100ft":	1,
        "deg/100m": 3.280839895,
        "deg/10m":	0.32808399,
        "deg/30ft":	0.3,
        "deg/30m":	0.984251969,
        "deg/ft":	0.01,
        "deg/m":	0.032808339,
        "rad/ft":	0.000174533,
        "rad/m":	0.000572615
    
        }
        
class Density(Quantity):
    """Represents a density quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the capacity.
        quantity (str): The unit of measurement for the capacity.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to barrels per foot.
    """

    def __init__(self, value, quantity):
        """Initializes a Density object.

        Args:
            value (float): The numerical value of the capacity.
            quantity (str): The unit of measurement for the capacity.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
            "lb/gal":	1,
            "Dap1":	1048.210387,
            "g/cm3":	0.119826427,
            "kg/l":	0.119826427,
            "kg/m3":	119.8264273,
            "lb/bbl":	42,
            "lb/ft3":	7.480519481,
            "lb/in3":	0.004329004,
            "psi/kft eq.":	51.94805195,
            "Sgair":	97.96143502,
            "Sgapi":	0.119944693,
            "ton/m3":	0.119826427,
            "kPa/m eq.":	1.175095833,
            "SG":	0.119826427
        }
        
class Energy(Quantity):
    """Represents an energy quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the capacity.
        quantity (str): The unit of measurement for the capacity.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to barrels per foot.
    """

    def __init__(self, value, quantity):
        """Initializes a Energy object.

        Args:
            value (float): The numerical value of the capacity.
            quantity (str): The unit of measurement for the capacity.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "N.m":	1,
        "Btu":	0.000947817,
        "cal":	0.238845897,
        "J":	1,
        "kcal":	0.002388846,
        "kJ":	0.001,
        "klbf.ft":	0.000737562,
        "KN.m": 0.001,
        "lbf.ft":	0.737562149
        }
        
class FluidPressure(Quantity):
    """Represents a fluid pressure quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the capacity.
        quantity (str): The unit of measurement for the capacity.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to barrels per foot.
    """

    def __init__(self, value, quantity):
        """Initializes a Fluid Pressure object.

        Args:
            value (float): The numerical value of the capacity.
            quantity (str): The unit of measurement for the capacity.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "psi":	1,
        "gf/100cm2":	7030.695796,
        "kPa":	6.894757293,
        "lbf/100ft2":	14400,
        "Pa":	6894.757293
        }

class FluidVolume(Quantity):
    """Represents a fluid volume quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Fluid Volume object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
            "bbl":	1,
            "Bcf":	5.61E-09,
            "ft3":	5.614583333,
            "m3":	0.158987,
            "Mbbl":	0.001,
            "MMbbl":	1.00E-06,
            "MMScf":	5.614583333,
            "Tscf":	5.61E-12
        }

class Force(Quantity):
    """Represents a force quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Force object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
            "klbf":	1,
            "daN":	444.8221615,
            "dyn":	444822161.5,
            "gf":	4535392.37,
            "kdaN":	0.444822162,
            "kdyn":	444822.1615,
            "kgf":	453.539237,
            "kN":	4.448221615,
            "lbf":	1000,
            "MN":	0.004448222,
            "N":	4448.221615,
            "tonf":	0.45359237,
            "tonne": 0.45359237,
        }

class Mass(Quantity):
    """Represents a mass quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Mass object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "klb":	1,
        "g":	453592.37,
        "kg":	453.59237,
        "lb":	1000,
        "ton":	0.45359237,
        "Ukton":	0.446428571,
        "Uston":	0.5
        }
        
class MudWeight(Quantity):
    """Represents a mud weight quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Mud Weight object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "lb/gal":	1,
        "bar/m eq.":	0.011750958,
        "g/cm3":	0.119826427,
        "kg/cm2.ft":	0.00365231,
        "kg/cm2.m":	0.011982643,
        "kg/m3":	119.8264273,
        "kPa/ft eq.":	0.35816921,
        "kPa/ft eq.":	1.175095833,
        "lb/bbl":	42,
        "lb/ft3":	7.480519481,
        "lb/in3":	0.004329004,
        "Pa/m eq.":	1175.095833,
        "ppg":	1,
        "psi/ft. eq.":	0.051948052,
        "psi/m eq.":	0.170433241,
        "SG":	0.119826427,
        }

class PumpPressure(Quantity):
    """Represents a pump pressure quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Pump Pressure object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "psi":	1,
        "bar":	0.068947573,
        "kPa":	6.894757293,
        "MPa":	0.006894757,
        "Pa":	6894.757293,
        }
    
class SaltConcentration(Quantity):
    """Represents a salt concentration quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Salt Concentration object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "lb/bbl":	1,
        "g/cm3":	9.00285301,
        "kg/m3":	2.853010174
        }
        
class Stress(Quantity):
    """Represents a stress quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Stress object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "psi":	1,
        "bar":	0.068947573,
        "kgf/cm2":	0.070306958,
        "kgf/m2":	703.0695796,
        "kPa":	6.894757293,
        "kpsi":	0.001,
        "lb/ft2":	144,
        "MPa":	0.006894757,
        "Pa":	6894.752729,
        "psf":	144,
        "N/mm2":	0.006894757,
        }
        
class Viscosity(Quantity):
    """Represents a viscosity quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Viscosity object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "cp":	1,
        "kPa.d":	1.16E-11,
        "mPa.s":	1,
        "Pa.s": 0.001,
        }

class Volume(Quantity):
    """Represents a volume quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Volume object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "ft3":	5.61458333333334,
        "acre.ft":	0.000128893097643098,
        "bbl":	1,
        "Bcf":	5.61458333333334E-09,
        "cm3":	158987.294928,
        "Gm3":	1.58987294928E-10,
        "galUK":	34.9723157544176,
        "galUS":	42,
        "km3":	1.58987294928E-10,
        "L":	158.987294928,
        "Mm3":	2.83E-08,
        "m3":	0.158987294928,
        "Mbbl":	0.001,
        "Mcf":	0.00561458333333334,
        "MgalUK":	0.0349723157544176,
        "MgalUS":	0.0420000000000001,
        "MMbbl":	0.000001,
        "MMcf":	 0.0000561458333333334,
        "MMgalUK":	0.0000349723157544176,
        "MMgalUS":	0.0000420000000000001,
        "MMrb":	0.000001,
        "MMscf":	5.61458E-06,
        "rb":	1,
        "rcf":	5.61458333333334,
        "scf":	5.61458333333334,
        "stb":	1,
        "Tcf":	5.61458333333334E-12,
        }

class Velocity(Quantity):
    """Represents a volume velocity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the velocity.
        quantity (str): The unit of measurement for the velocity.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Velocity object.

        Args:
            value (float): The numerical value of the velocity.
            quantity (str): The unit of measurement for the velocity
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
            "ft/min":	1,
            "cm/day":	43891.2,
            "cm/h":	1828.8,
            "cm/ms":	0.000508,
            "cm/s":	0.508,
            "cm/yr":	16031260.8,
            "d/ft eq.":	0.000694444,
            "d/km eq.":	2.278361038,
            "d/m eq.":	0.002278361,
            "ft/d":	1440,
            "ft/hr":	60,
            "ft/ms":	1.67E-05,
            "ft/s":	0.016666667,
            "ft/yr":	525960,
            "km/h":	0.018288,
            "km/s":	5.08E-06,
            "m/d":	438.912,
            "m/hr":	18.288,
            "m/min":	0.3048,
            "m/ms":	5.08E-06,
            "m/s":	0.00508,
            "m/yr":	160312.608,
            "mi/hr":	0.011363636,
            "ms/cm eq.":	1968.503937,
            "ms/m eq":	196850.3937,
            "s/cm eq.":	1.968503937,
            "s/ft eq.":	60,
            "s/m eq.":	196.8503937,
        }

class UnitCapacity(Quantity):
    """Represents a unitcapacity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the unitcapacity.
        quantity (str): The unit of measurement for the unitcapacity.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Velocity object.

        Args:
            value (float): The numerical value of the velocity.
            quantity (str): The unit of measurement for the velocity
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "bbl/ft":	1,
        "USgal/ft":	42.00002354,
        "USgal/m":	137.7950849,
        "bbl/m":	3.280839895,
        "ft3/ft":	5.614575335,
        "l/m":	521.6108924,
        "m3/m":	0.521610892,
        }

class FlowRate(Quantity):
    """Represents a flow rate quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the flow rate.
        quantity (str): The unit of measurement for the flow rate.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Flow rate object.

        Args:
            value (float): The numerical value of the flow rate.
            quantity (str): The unit of measurement for the flow rate.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "gal/min":	1,
        "bbl/day": 32.28571429,
        "bbl/min":	0.023809524,
        "ft3/day":	192.5,
        "ft3/sec":	0.002228009,
        "Mm3/day":	5.45E-06,
        "m3/day":	5.450992969,
        "m3/sec":	6.31E-05,
        "Mbbl/day":	0.034285715,
        "MMscf/day":	1.93E-04,
        "Mscf/day": 0.1925,
        "m3/min":	3.79E-03,
        "l/min":	3.785411784,
        "l/s":	6.31E-02,
        "galUS/min": 1,
        "galUK/min": 1,
        }

class WeightonBit(Quantity):
    """Represents a weight on bit quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Weight on Bit object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "klbf":	1,
        "dyn":	444822161.5,
        "kgf":	3453.59237,
        "lbf":	1000,
        "N":	4448.221616,
        "tonf":	0.45359237,
        "kN":	4.448221615,
        "daN":	444.8221615,
        "kdaN":	0.444822162,
        "kdyn":	444822.1615,
        }
        
class WeightperLength(Quantity):
    """Represents a weight per length quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Weight per Length object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
        "lb/bbl":	1,
        "g/cm3":	9.00285301,
        "kg/m3":	2.853010174
        }

class Temperature(Quantity):
    """Represents a salt concentration quantity with conversion capabilities.

    Attributes:
        value (float): The numerical value of the pressure.
        quantity (str): The unit of measurement for the pressure.
        conversion_factors (dict): A dictionary mapping unit names to their conversion factors relative to pascals.
    """

    def __init__(self, value, quantity):
        """Initializes a Salt Concentration object.

        Args:
            value (float): The numerical value of the pressure.
            quantity (str): The unit of measurement for the pressure.
        """
        super().__init__(value, quantity)

        self.conversion_factors = {
            "degC": 1,
            "degK": 273.15,
            "R": 491.67,
            "degF": 33.8
        }

    def to_celsius(self):
        return self.to_unit("degC")

    def to_kelvin(self):
        return self.to_unit("degK")

    def to_rankine(self):
        return self.to_unit("R")

    def to_fahrenheit(self):
        return self.to_unit("degF")      
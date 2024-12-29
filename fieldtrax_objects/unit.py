import math;

class Unit:
    """A base class for all units."""
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __repr__(self):
        return f"{self.value} {self.unit}"
    
def calculate_thickness(outer_diameter, inner_diameter, thickness_unit, precision = 2):
    """Calculates the thickness of a cylindrical object.

    Args:
        outer_diameter (WellboreDiameter): The outer diameter of the object.
        inner_diameter (WellboreDiameter): The inner diameter of the object.

    Returns:
        WellboreDiameter: The thickness of the object.
    """
    # if outer_diameter.unit != inner_diameter.unit:
    #     raise ValueError("Outer and inner diameters must have the same units")

    # thickness_value = outer_diameter.value - inner_diameter.value
    # thickness_unit = outer_diameter.unit

    # return Wellbore_Diameter(thickness_value, thickness_unit).format(thickness_unit, precision)
    
    if outer_diameter.__class__ != inner_diameter.__class__:
        raise ValueError("Outer and inner diameters must have the same units for initial conversion")

    # Convert both diameters to the desired thickness unit
    outer_diameter_in_thickness_unit = outer_diameter.to_unit(thickness_unit)
    inner_diameter_in_thickness_unit = inner_diameter.to_unit(thickness_unit)

    thickness_value = outer_diameter_in_thickness_unit - inner_diameter_in_thickness_unit

    return Wellbore_Diameter(thickness_value, thickness_unit)#.format(thickness_unit, precision)

class Wellbore_Diameter(Unit):
    """Represents a unit of Wellbore diameter.""" 
    conversion_factors = {
        "millimeters": 25.4,
        "inches": 1,
        "centimeters": 2.54,
        "meters": 0.0254,
        "feet": 0.08333333,
        # Add more units and conversion factors as needed
    }
    
def convert_to_all_units(self, precision = 2):
        """Converts the value to all available units.

        Returns:
            list: A list of tuples containing the converted value and unit.
        """
        results = []
        for unit in self.conversion_factors.keys():
            converted_value = self.to_unit(unit)
            results.append((round(converted_value,precision), unit))
        return results
    
def format(self, unit, precision=2, rounding_mode="ROUND_HALF_UP"):
        """Formats the wellbore diameter to a specified unit with precision."""
        formatted_value = self.to_unit(unit)  # Assuming it returns a float
        rounded_value = round(formatted_value, precision)
        return f"{rounded_value:.{precision}f} {self.unit}"
    
def to_inches(self):
        """Converts the wellbore diameter to inches."""
        return self.value * self.conversion_factors[self.unit]
    
def to_unit(self, unit):
        """Converts the wellbore_diameter to a specified unit."""
        if self.unit != unit:
            inches = self.to_inches()
            converted_value = inches * self.conversion_factors[unit]
            return converted_value
        return self.value  # Return only the numeric value

def __add__(self, other):
        """Adds two wellbore Diameters."""
        if self.unit != other.unit:
            raise ValueError("Cannot add wellbore Diameters with different units")
        return Wellbore_Diameter(self.value + other.value, self.unit)

def __sub__(self, other):
        """Subtracts two wellbore Diameters"""
        if self.unit != other.unit:
            raise ValueError("Cannot subtract wellbore Diameters with different units")
        return Wellbore_Diameter(self.value - other.value, self.unit)

def __mul__(self, other):
        """Multiplies a wellbore Diameters by a scalar."""
        return Wellbore_Diameter(self.value * other, self.unit)

def __truediv__(self, other):
        """Divides a wellbore Diameters by a scalar."""
        return Wellbore_Diameter(self.value / other, self.unit)

def __eq__(self, other):
        """Compares two wellbore Diameters."""
        if self.unit != other.unit:
            return False
        return self.value == other.value
    

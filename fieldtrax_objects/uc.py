class UnitConverter:
    """A simple unit converter class."""

    conversion_factors = {
        "meters": {
            "centimeters": 100,
            "inches": 39.3701,
            "feet": 3.28084,
            "yards": 1.09361,
            "meters": 1
            
        },
        "kilograms": {
            "grams": 1000,
            "pounds": 2.20462,
            "ounces": 35.274
        },
        "liters": {
            "milliliters": 1000,
            "gallons": 0.264172,
            "quarts": 1.05669
        }
    }

    def convert(self, value, from_unit, to_unit):
        """Converts a value from one unit to another.

        Args:
            value (float): The value to convert.
            from_unit (str): The unit of the input value.
            to_unit (str): The desired unit of the output value.

        Returns:
            The converted value.
        """

        if from_unit not in self.conversion_factors or to_unit not in self.conversion_factors[from_unit]:
            raise ValueError("Invalid units.")

        conversion_factor = self.conversion_factors[from_unit][to_unit]
        return value * conversion_factor

if __name__ == "__main__":
    converter = UnitConverter()

    value = 10
    from_unit = "centimeters"
    to_unit = "feet"

    converted_value = converter.convert(value, from_unit, to_unit)
    print(f"{value} {from_unit} is equal to {converted_value} {to_unit}")
from quantity import (Diameter, Length, Depth, FlowRate, Velocity, UnitCapacity, 
                      Volume,LinearDensity, Pressure,Torque
)
from constants import ( ZERO_VOLUME, ZERO_LENGTH, ZERO_DIAMETER, ZERO_DEPTH,
                        internal_depth_unit, internal_length_unit, internal_diameter_unit,
                        internal_velocity_unit, internal_flowrate_unit, Internal_unitcapacity_unit
)
from pipe import Pipe

class Tool(Pipe):
    def __init__(self, outer_diameter: Diameter, inner_diameter: Diameter, length: Length, starting_depth:Depth=None,
                 linear_density: LinearDensity=None, yield_strength: Pressure=None, grade: str=None,
                 thread: str=None, torque: Torque=None, burst: Pressure=None, collapse: Pressure=None):
        super().__init__(outer_diameter, inner_diameter, length, starting_depth,
                 linear_density, yield_strength, grade,thread, torque, burst, collapse)
        self.long_name = "Tool"
        self.short_name = "tl"

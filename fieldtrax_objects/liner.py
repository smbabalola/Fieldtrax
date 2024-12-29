from quantity import (Diameter, Length, Depth, FlowRate, Velocity, UnitCapacity, 
                      Volume,LinearDensity, Pressure,Torque
)
from constants import ( ZERO_VOLUME, ZERO_LENGTH, ZERO_DIAMETER, ZERO_DEPTH,
                        internal_depth_unit, internal_length_unit, internal_diameter_unit,
                        internal_velocity_unit, internal_flowrate_unit, Internal_unitcapacity_unit
)
from pipe import Pipe

class Liner(Pipe):
    def __init__(self, outer_diameter: Diameter, inner_diameter: Diameter, length: Length, starting_depth:Depth,
                 linear_density: LinearDensity=None, yield_strength: Pressure=None, grade: str=None,
                 thread: str=None, torque: Torque=None, burst: Pressure=None, collapse: Pressure=None):
        super().__init__(outer_diameter, inner_diameter, length, starting_depth, linear_density, yield_strength, grade,
                 thread, torque, burst, collapse)
        self.long_name = "Liner"
        self.short_name = "lnr"
        #these properties are set when a liner is below casing
        self.liner_installed_below = False
        self.top_of_liner = ZERO_DEPTH 
        self.liner_od = ZERO_DIAMETER
        self.liner_id = ZERO_DIAMETER
        self.liner_length = ZERO_DIAMETER

    def overlap(self, previous_shoe:Pipe) -> Length:
        starting_depth_in_ft = self.start_depth.to_unit(internal_depth_unit)
        # end_depth_in_ft = self.end_depth().to_unit(internal_depth_unit)
        previous_shoe_depth_in_ft = previous_shoe.end_depth().to_unit(internal_depth_unit)
        
        internal_value = previous_shoe_depth_in_ft - starting_depth_in_ft
        return Depth(internal_value, "ft")
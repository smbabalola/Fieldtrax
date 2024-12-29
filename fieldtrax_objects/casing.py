from quantity import (Diameter, Length, Depth, FlowRate, Velocity, UnitCapacity, 
                      Volume,LinearDensity, Pressure,Torque
)

from constants import ( ZERO_VOLUME, ZERO_LENGTH, ZERO_DIAMETER, ZERO_DEPTH,
                        internal_depth_unit, internal_length_unit, internal_diameter_unit,
                        internal_velocity_unit, internal_flowrate_unit, Internal_unitcapacity_unit
)

from pipe import Pipe

class Casing(Pipe):
    def __init__(self, outer_diameter: Diameter, inner_diameter: Diameter, length: Length, starting_depth:Depth=ZERO_DEPTH,
                 linear_density: LinearDensity=None, yield_strength: Pressure=None, grade: str=None,
                 thread: str=None, torque: Torque=None, burst: Pressure=None, collapse: Pressure=None):
        super().__init__(outer_diameter, inner_diameter, length, starting_depth, linear_density, yield_strength, 
                         grade, thread, torque, burst, collapse)
        self.long_name = "Casing"
        self.short_name = "csg"
        #these properties are set when a liner is below casing
        # self.liner_installed_below = False
        # self.top_of_liner = zero_volume 
        # self.liner_od = zero_in
        # self.liner_id = zero_in
        # self.liner_length = zero_ft
        
    # def casing_Volume(self, top_of_liner: Depth= zero_ft)->Volume: 
    #     if top_of_liner == zero_ft:
    #         return self.pipe_volume()
    #     inner_diameter_in_inches = self.inner_diameter.to_unit(internal_diameter_unit)
    #     internal_value =((inner_diameter_in_inches) ** 2) /1029.4
    #     length_in_ft = top_of_liner - self.starting_depth        
        
    #     internal_value = internal_value * length_in_ft
    #     return Volume(internal_value,"bbl")
        
        
    # def liner_lap(self) -> Length:
    #     if (self.liner_installed_below == False):
    #         raise ValueError("No liners below casing!")
    #     starting_depth_in_ft = self.top_of_liner.to_unit(internal_depth_unit)
    #     end_depth_in_ft = self.end_depth.to_unit(internal_depth_unit)

    #     internal_value = end_depth_in_ft - starting_depth_in_ft
    #     return Depth(internal_value, "ft")











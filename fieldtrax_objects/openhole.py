from quantity import (Diameter, Length, Depth, FlowRate, Velocity, UnitCapacity, 
                      Volume,LinearDensity, Pressure,Torque
)
from constants import ( ZERO_VOLUME, ZERO_LENGTH, ZERO_DIAMETER, ZERO_DEPTH,
                        internal_depth_unit, internal_length_unit, internal_diameter_unit,
                        internal_velocity_unit, internal_flowrate_unit, internal_unitcapacity_unit
)
from pipe import Pipe

class OpenHole():
    def __init__(self, inner_diameter: Diameter, start_depth: Depth,
                 end_depth: Depth, main_hole=False):
        self.long_name = "Hole"
        self.short_name = "oh"
        self.inner_diameter = inner_diameter
        self.start_depth = start_depth
        self.end_depth = end_depth
        self.main_hole = main_hole
        self.casedoff = False
        # self.casing = []
        # self.liner = []

    def open_hole_area(self) -> UnitCapacity:
        inner_diameter_in_inches = self.inner_diameter.to_unit(internal_diameter_unit)
        
        internal_value =((inner_diameter_in_inches) ** 2) /1029.4
        internal_quantity = UnitCapacity(internal_value, "bbl/ft")
        return internal_quantity
    
    def open_hole_volume(self, iter_current_depth: Depth = ZERO_DEPTH)->Volume:
        #note iteration start depth
        open_hole_area_in_bblperft = self.open_hole_area().to_unit(internal_unitcapacity_unit) 
        iter_current_depth_in_ft = iter_current_depth.to_unit("ft")
        start_depth_in_ft = self.start_depth.to_unit("ft")
        end_depth_in_ft = self.end_depth.to_unit("ft")
        length_in_ft = end_depth_in_ft - start_depth_in_ft        
        if iter_current_depth_in_ft >= start_depth_in_ft:
            length_in_ft = end_depth_in_ft - iter_current_depth_in_ft
        internal_value = open_hole_area_in_bblperft * length_in_ft
        internal_quantity = Volume(internal_value,"bbl")
        return internal_quantity
    
    def section_length(self)->Depth:
        start_depth_in_ft = self.start_depth.to_unit(internal_depth_unit)    
        end_depth_in_ft = self.end_depth.to_unit(internal_depth_unit)
        
        internal_value = end_depth_in_ft - start_depth_in_ft
        internal_quantity = Depth(internal_value, internal_depth_unit)
        return internal_quantity
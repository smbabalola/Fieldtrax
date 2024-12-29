from quantity import Diameter, Length, Depth, FlowRate, Velocity, UnitCapacity, Volume,LinearDensity, Pressure,Torque
import math
import constants 
from constants import ( ZERO_VOLUME, ZERO_LENGTH, ZERO_DIAMETER, ZERO_DEPTH
)

internal_depth_unit = "ft"
internal_length_unit = "ft"
internal_diameter_unit = "in"
internal_velocity_unit = "ft/min"
internal_flowrate_unit = "bbl/min"
internal_unitcapacity_unit = "bbl/ft"

class Pipe:
    def __init__(self, outer_diameter: Diameter, inner_diameter: Diameter, length: Length, start_depth:Depth=
                 Depth(0,"ft"), linear_density: LinearDensity=None, yield_strength: Pressure=None, grade: str=None, thread: str=None, 
                 torque: Torque=None, burst: Pressure=None, collapse: Pressure=None):
        if inner_diameter.format("in") >= outer_diameter.format("in"):
            raise ValueError("inner diameter cannot be greater than outerdiameter.")
        self.long_name = "Pipe"
        self.short_name = "Pipe"
        self.outer_diameter = outer_diameter
        self.inner_diameter = inner_diameter
        self.start_depth = start_depth
        self.length = length
        self.linear_density = linear_density
        self.yield_strength = yield_strength
        self.grade = grade
        self.thread = thread
        self.torque = torque
        self.burst = burst
        self.collapse = collapse
        
    def end_depth(self)-> Depth:  
        start_depth_in_ft = self.start_depth.to_unit(internal_depth_unit)
        length_in_ft = self.length.to_unit(internal_length_unit)  
              
        internal_value = start_depth_in_ft +length_in_ft
        return Depth(internal_value, "ft")                     

    def pipe_area(self) -> UnitCapacity:
        inner_diameter_in_inches = self.inner_diameter.to_unit(internal_diameter_unit)
        
        internal_value =((inner_diameter_in_inches) ** 2) /1029.4
        internal_quantity = UnitCapacity(internal_value, "bbl/ft")
        return internal_quantity
    
    def pipe_volume(self, iter_current_depth:Depth= ZERO_DEPTH)->Volume:
        pipe_area_in_bblperft = self.pipe_area().to_unit(internal_unitcapacity_unit)
        iter_current_depth_in_ft = iter_current_depth.to_unit("ft")
        length_in_ft = self.length.to_unit(internal_depth_unit)       
        
        start_depth_in_ft = self.start_depth.to_unit("ft")
        end_depth_in_ft = self.end_depth().to_unit("ft")
        length_in_ft = end_depth_in_ft - start_depth_in_ft        
        if iter_current_depth_in_ft >= start_depth_in_ft:
            length_in_ft = end_depth_in_ft - iter_current_depth_in_ft

        internal_value = pipe_area_in_bblperft * length_in_ft
        internal_quantity = Volume(internal_value,"bbl")
        return internal_quantity
    
    def pipe_displacement_area(self) -> UnitCapacity:
        outer_diameter_in_inches = self.outer_diameter.to_unit(internal_diameter_unit)
        inner_diamter_in_inches = self.inner_diameter.to_unit(internal_diameter_unit)

        internal_value = (((outer_diameter_in_inches/2)**2)-((inner_diamter_in_inches/2) ** 2))/1029.4
        internal_quantity = UnitCapacity(internal_value, "bbl/ft")
        return internal_quantity
    
    def string_velocity(self, flow_rate)->Velocity:
        pipe_area_in_bblperft = self.pipe_area().format(internal_unitcapacity_unit)        
        flow_rate_in_bblpermin = flow_rate.to_unit(internal_flowrate_unit)
        
        internal_value = pipe_area_in_bblperft/flow_rate_in_bblpermin
        internal_quantity = Velocity(internal_value,"ft/min")
        return internal_quantity

    def pipe_displacement_volume(self) -> Volume:
        pipe_displacement_area_in_bblperft = self.pipe_displacement_area().format(internal_unitcapacity_unit)
        length_in_ft = self.length.to_unit(internal_depth_unit)
        
        internal_value = pipe_displacement_area_in_bblperft * length_in_ft
        internal_quantity = Volume(internal_value,"bbl")
        return internal_quantity
    
    def drift(self):
        pass  

class Tool(Pipe):
    def __init__(self, outer_diameter: Diameter, inner_diameter: Diameter, length: Length, starting_depth:Depth=None,
                 linear_density: LinearDensity=None, yield_strength: Pressure=None, grade: str=None,
                 thread: str=None, torque: Torque=None, burst: Pressure=None, collapse: Pressure=None):
        super().__init__(outer_diameter, inner_diameter, length, starting_depth,
                 linear_density, yield_strength, grade,thread, torque, burst, collapse)
        self.long_name = "Tool"
        self.short_name = "tl"


# class Pit:
#     def __init__(self, id, name):
#         self.id = id
#         self.name = name
#         self.statue = ""
#         self.fluid_type = ""
#         self._volume = ureg.Quantity(volume,unit_volume)

#     def volume(self):
#         return self._volume

#     def volume(self, value):
#         self._volume = ureg.Quantity(value,unit_volume)

    # def capacity(self, capacity_unit="barrels per foot"):
    #     inner_diameter_in_inches = self.inner_diameter.to_unit(internal_diameter_unit)
    
    #     internal_value = ((inner_diameter_in_inches**2)/1029.4)
    #     internal_quantity = Capacity(internal_value, capacity_unit)
    #     return Capacity(internal_quantity.to_unit(capacity_unit), capacity_unit)
    
    # def volume(self, volume_unit= "barrels"):
    #     internal_length_unit = "feet"
    #     internal_capacity_unit = "barrels per foot"
    
    #     internal_value = self.length.to_unit(internal_length_unit) * Pipe.capacity(capacity_unit=internal_capacity_unit)
    #     internal_quantity = Volume(internal_value, volume_unit)
    #     return Volume(internal_quantity.to_unit(volume_unit), volume_unit)
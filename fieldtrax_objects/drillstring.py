from quantity import (Diameter, Length, Depth, FlowRate, Velocity, UnitCapacity, 
                      Volume,LinearDensity, Pressure,Torque
)
from constants import ( ZERO_VOLUME, ZERO_LENGTH, ZERO_DIAMETER, ZERO_DEPTH,
                        internal_depth_unit, internal_length_unit, internal_diameter_unit,
                        internal_velocity_unit, internal_flowrate_unit, Internal_unitcapacity_unit
)
from pipe import Pipe
from tool import Tool
from casing import Casing
from openhole import OpenHole

class DrillString:
    def __init__(self):
        self.components = []

    def add_component(self, component: Tool):
        self.components.append(component)

    def string_volume(self) -> Volume:
        total_volume = Volume(0, "bbl")
        
        for component in self.components:
            total_volume += component.pipe_volume()
        return total_volume

    def annular_volume(self, last_casing: Casing, liners: list, open_hole: OpenHole) -> Volume:
        total_volume = Volume(0, "bbl")
        for component in self.components:
            component_start_depth = component.start_depth.to_unit(internal_depth_unit)
            component_end_depth = component.end_depth().to_unit(internal_depth_unit)

            # Check if the component is within the last casing
            casing_start_depth = last_casing.start_depth.to_unit(internal_depth_unit)
            casing_end_depth = last_casing.end_depth().to_unit(internal_depth_unit)
            if component_start_depth >= casing_start_depth and component_end_depth <= casing_end_depth:
                annular_area = (last_casing.inner_diameter.to_unit(internal_diameter_unit) ** 2 - component.outer_diameter.to_unit(internal_diameter_unit) ** 2) / 1029.4
                total_volume += Volume(annular_area * component.length.to_unit(internal_length_unit), "bbl")
                continue

            # Check if the component is within any liner
            for liner in liners:
                liner_start_depth = liner.starting_depth.to_unit(internal_depth_unit)
                liner_end_depth = liner.end_depth().to_unit(internal_depth_unit)
                if component_start_depth >= liner_start_depth and component_end_depth <= liner_end_depth:
                    annular_area = (liner.inner_diameter.to_unit(internal_diameter_unit) ** 2 - component.outer_diameter.to_unit(internal_diameter_unit) ** 2) / 1029.4
                    total_volume += Volume(annular_area * component.length.to_unit(internal_length_unit), "bbl")
                    break
            else:
                # Check if the component is within the open hole
                open_hole_start_depth = open_hole.start_depth.to_unit(internal_depth_unit)
                open_hole_end_depth = open_hole.end_depth.to_unit(internal_depth_unit)
                if component_start_depth >= open_hole_start_depth and component_end_depth <= open_hole_end_depth:
                    annular_area = (open_hole.inner_diameter.to_unit(internal_diameter_unit) ** 2 - component.outer_diameter.to_unit(internal_diameter_unit) ** 2) / 1029.4
                    total_volume += Volume(annular_area * component.length.to_unit(internal_length_unit), "bbl")

        return total_volume

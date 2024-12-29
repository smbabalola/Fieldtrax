from quantity import Diameter, Length, Depth, FlowRate, Velocity, UnitCapacity, Volume
import math
internal_depth_unit = "ft"
internal_diameter_unit = "in"
internal_velocity_unit = "ft/min"
internal_flowrate_unit = "bbl/min"
internal_unitcapacity_unit = "bbl/ft"

internal_azimuth_unit = "degree"
internal_area_unit = "square meters"
internal_volume_unit = "cubic meters"
internal_weight_unit = "kilograms"
internal_torque_unit = "joules"
internal_capacity_unit = "bbl/ft"

class Section:
    def __init__(self, section_name: str, annular_od: Diameter=0, annular_id:Diameter=0, start_depth:Depth=0, end_depth: Depth=0, tool_od:Diameter=0, tool_id:Diameter=0):
        self.section_name = section_name
        self.annular_od = annular_od
        self.annular_id = annular_id
        # self._section_length = ureg.Quantity(section_length, unit_depth)
        self.start_depth = start_depth
        self.end_depth = end_depth
        self.tool_od = tool_od
        self.tool_id = tool_id

    def annular_velocity(self,flow_rate:FlowRate=0)->Velocity:
        annular_area_in_bblperft = self.annular_area().to_unit(internal_capacity_unit)
        # annular_area_in_bblperft = UnitCapacity(self.annular_area().value, internal_capacity_unit)        
        flow_rate_in_bblpermin = flow_rate.to_unit(internal_flowrate_unit)
        
        internal_value = annular_area_in_bblperft/flow_rate_in_bblpermin
        internal_quantity = Velocity(internal_value,"ft/min")
        return internal_quantity

    def string_velocity(self, flow_rate)->Velocity:
        # string_area_in_bblperft = UnitCapacity(self.string_area().value, internal_capacity_unit)
        string_area_in_bblperft = self.string_area()(internal_capacity_unit)        
        flow_rate_in_bblpermin = flow_rate.to_unit(internal_flowrate_unit)
        
        internal_value = string_area_in_bblperft/flow_rate_in_bblpermin
        internal_quantity = Velocity(internal_value,"ft/min")
        return internal_quantity
        
    def annular_area(self)->UnitCapacity:
        annular_od_in_inches = self.annular_od.to_unit(internal_diameter_unit)
        annular_id_in_inches = self.annular_id.to_unit(internal_diameter_unit)
                                                    
        internal_value = ((((annular_od_in_inches)**2)-((annular_id_in_inches) ** 2)))/1029.4
        internal_quantity = UnitCapacity(internal_value, "bbl/ft")
        return internal_quantity

    def annular_volume(self)->Volume:
        # annular_area_in_bblperft = UnitCapacity(self.annular_area().value, internal_capacity_unit)
        annular_area_in_bblperft = self.annular_area().to_unit(internal_capacity_unit)
        # section_length_in_ft = Depth(self.section_length(),internal_depth_unit)
        section_length_in_ft = self.section_length().to_unit(internal_depth_unit)
        print(f"Section Length in ft: {section_length_in_ft}")
        internal_value = annular_area_in_bblperft * section_length_in_ft
        internal_quantity = Volume(internal_value,"bbl")
        return internal_quantity
    
    def string_area(self) ->UnitCapacity:
        tool_id_in_inches = self.tool_id.to_unit(internal_diameter_unit)
        
        internal_value =((tool_id_in_inches) ** 2)/1029.4
        internal_quantity = UnitCapacity(internal_value, "bbl/ft")
        return internal_quantity

    def string_volume(self)->Volume:
        # string_area_in_bblperft = UnitCapacity(self.string_area().value, internal_capacity_unit)
        string_area_in_bblperft = self.string_area().to_unit(internal_capacity_unit)
        # section_length_in_ft = Depth(self.section_length(),internal_depth_unit)
        section_length_in_ft = self.section_length().to_unit(internal_depth_unit)        
        
        internal_value = string_area_in_bblperft * section_length_in_ft
        internal_quantity = Volume(internal_value,"bbl")
        return internal_quantity

    def pipe_displacement_area(self) -> UnitCapacity:
        tool_od_in_inches = self.tool_od.to_unit(internal_diameter_unit)
        tool_id_in_inches = self.tool_id.to_unit(internal_diameter_unit)

        internal_value = (((tool_od_in_inches)**2)-((tool_id_in_inches) ** 2))/1029.4
        internal_quantity = UnitCapacity(internal_value, "bbl/ft")
        return internal_quantity        
        
    def pipe_displacement_volume(self) -> Volume:
        # pipe_displacement_area_in_bblperft = UnitCapacity(self.pipe_displacement_area().value, internal_capacity_unit)
        # section_length_in_ft = Depth(self.section_length(),internal_depth_unit)
        
        pipe_displacement_area_in_bblperft = self.pipe_displacement_area().to_unit(internal_capacity_unit)
        section_length_in_ft = self.section_length().to_unit(internal_depth_unit)
        
        internal_value = pipe_displacement_area_in_bblperft * section_length_in_ft
        internal_quantity = Volume(internal_value,"bbl")
        return internal_quantity

    def section_length(self)->Depth:
        start_depth_in_ft = self.start_depth.to_unit(internal_depth_unit)    
        end_depth_in_ft = self.end_depth.to_unit(internal_depth_unit)
        
        internal_value = -(start_depth_in_ft - end_depth_in_ft)
        internal_quantity = Depth(internal_value, internal_depth_unit)
        # return Diameter(internal_quantity.to_unit(thickness_unit), thickness_unit)
        return internal_quantity
    
    def string_velocity(self):
        pass
    
    def slip_velocity(self):
        pass
    
    def critical_annular_velocity(self):
        pass

    def critical_flow_rate(self):
        pass
        
    # def holevolumecalculator(casing, liner, openhole, drillpipe):
    #     # initialize variables
    #     total_volume = 0
    #     section_volumes = []
    #     annular_volumes = []
    #     previous_outer_diameter = 0
    #     previous_inner_diameter = 0

    #     # calculate volume for each casing section
    #     for section in casing:
    #         section_volume = 0
    #         annular_volume = 0
    #         if section['OD'] > previous_inner_diameter:
    #             section_volume = (section['OD']**2 - section['ID']**2) / 1029.4 * section['depth']
    #             if previous_outer_diameter > 0:
    #                 annular_volume = (previous_outer_diameter**2 - section['OD']**2) / 1029.4 * section['depth']
    #             previous_outer_diameter = section['OD']

    #             previous_inner_diameter = section['ID']
    #         section_volumes.append(section_volume)
    #         annular_volumes.append(annular_volume)
    #         total_volume += section_volume + annular_volume

    #     # calculate volume for each liner section
    #     for section in liner:
    #         section_volume = (section['OD']**2 - section['ID']**2) / 1029.4 * section['depth']
    #         section_volumes.append(section_volume)
    #         total_volume += section_volume

    #     # calculate volume for open hole
    #     openhole_volume = (openhole['OD']**2 - openhole['ID']**2) / 1029.4 * openhole['depth']
    #     section_volumes.append(openhole_volume)
    #     total_volume += openhole_volume

    #     # calculate volume for drill pipe in hole
    #     if drillpipe:
    #         drillpipe_volume = (drillpipe['OD']**2 - drillpipe['ID']**2) / 1029.4 * (openhole['depth'] - drillpipe['depth'])
    #         section_volumes.append(drillpipe_volume)
    #         total_volume += drillpipe_volume

    #     # calculate displacement volume for drill pipe in hole
    #     if drillpipe:
    #         displacement_volume = (drillpipe['OD']**2 - drillpipe['ID']**2) / 1029.4 * drillpipe['depth']
    #         total_volume -= displacement_volume

    #     return total_volume, section_volumes, annular_volumes


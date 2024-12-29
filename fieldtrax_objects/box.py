from quantity import Length, Area, Volume, Depth, Diameter, LinearDensity, Weight, Pressure, Torque,Capacity
internal_length_unit = "ft"
internal_diameter_unit = "in"
internal_azimuth_unit = "degree"
internal_area_unit = "square meters"
internal_volume_unit = "cubic meters"
internal_weight_unit = "kilograms"
internal_torque_unit = "joules"
internal_capacity_unit = "barrels per foot"

class Box:
    def __init__(self, length: Length, width: Length, height: Length):
        self.length = length
        self.width = width
        self.height = height

    def perimeter(self, perimeter_unit="inches") -> Length:
        # internal_length_unit = "inches"
        length_in_inches = self.length.to_unit(internal_length_unit)    
        width_in_inches = self.width.to_unit(internal_length_unit)
        height_in_inches = self.height.to_unit(internal_length_unit)
        
        internal_value = 4 * (length_in_inches + width_in_inches + height_in_inches)
        internal_quantity = Length(internal_value, "inches")
        
        return Length(internal_quantity.to_unit(perimeter_unit), perimeter_unit)
        
    def area(self, area_unit="square inches") -> Area:
        # internal_length_unit = "inches"
        
        length_in_inches = self.length.to_unit(internal_length_unit)    
        width_in_inches = self.width.to_unit(internal_length_unit)
        height_in_inches = self.height.to_unit(internal_length_unit)
        
        internal_value_sqin = 2 * (length_in_inches * width_in_inches + length_in_inches * height_in_inches + width_in_inches * height_in_inches)
        internal_quantity_sqin = Area(internal_value_sqin, "square inches")
        internal_quantity = Area(internal_quantity_sqin.to_unit(internal_area_unit), internal_area_unit)
        return Area(internal_quantity.to_unit(area_unit), area_unit)
 
    def volume(self, volume_unit="cubic feet") -> Volume:
        # internal_unit = "meters"
        
        length_in_inches = self.length.to_unit(internal_length_unit)    
        width_in_inches = self.width.to_unit(internal_length_unit)
        height_in_inches = self.height.to_unit(internal_length_unit)
        
        internal_value = (length_in_inches * width_in_inches * height_in_inches)
        internal_quantity = Volume(internal_value, "cubic inches")
        return Volume(internal_quantity.to_unit(volume_unit), volume_unit)

class Pipe:
    def __init__(self, outer_diameter: Diameter, inner_diameter: Diameter, length: Length,
                 linear_density: LinearDensity, yield_strength: Pressure, grade: str,
                 thread: str, torque: Torque, burst: Pressure, collapse: Pressure):
        self.outer_diameter = outer_diameter
        self.inner_diameter = inner_diameter
        self.length = length
        self.linear_density = linear_density
        self.yield_strength = yield_strength
        self.grade = grade
        self.thread = thread
        self.torque = torque
        self.burst = burst
        self.collapse = collapse
        
    def capacity(self, capacity_unit="barrels per foot"):
        # internal_diameter_unit = "inches"
        
        # outer_diameter_in_inches = outer_diameter.to_unit(internal_diameter_unit)    
        inner_diameter_in_inches = self.inner_diameter.to_unit(internal_diameter_unit)
        
        internal_value = ((inner_diameter_in_inches**2)/1029.4)
        internal_quantity = Capacity(internal_value, capacity_unit)
        return Capacity(internal_quantity.to_unit(capacity_unit), capacity_unit)
    
    def volume(self, volume_unit= "barrels"):
        internal_length_unit = "feet"
        internal_capacity_unit = "barrels per foot"
    
        internal_value = self.length.to_unit(internal_length_unit) * Pipe.capacity(capacity_unit=internal_capacity_unit)
        internal_quantity = Volume(internal_value, volume_unit)
        return Volume(internal_quantity.to_unit(volume_unit), volume_unit)
    
    def drift(self):
        pass  
    
# class Section:
#     def __init__(self, section_name, annular_od, annular_id, start_depth, end_depth, tool_od, tool_id):
#         self._section_name = section_name
#         self._annular_od = Quantity(annular_od, unit_diameter)
#         self._annular_id = Quantity(annular_id, unit_diameter)
#         # self._section_length = ureg.Quantity(section_length, unit_depth)
#         self.start_depth = Quantity(start_depth, unit_depth)
#         self.end_depth = Quantity(end_depth, unit_depth)
#         self._tool_od = Quantity(tool_od, unit_diameter)
#         self._tool_id = Quantity(tool_id, unit_diameter)

#     @property
#     def section_name(self):
#         return self._section_name

#     @section_name.setter
#     def section_name(self, value):
#         self._section_name = value

#     @property
#     def annular_od(self):
#         return self._annular_od

#     @annular_od.setter
#     def annular_od(self, value):
#         self._annular_od = Quantity(value, unit_diameter)

#     @property
#     def annular_id(self):
#         return self._annular_id

#     @annular_id.setter
#     def annular_id(self, value):
#         self._annular_id = Quantity(value, unit_diameter)

#     @property
#     def section_length(self):
#         return self.end_depth - self.start_depth

#     @property
#     def tool_od(self):
#         return self._tool_od

#     @tool_od.setter
#     def tool_od(self, value):
#         self._tool_od = value

#     @property
#     def tool_id(self):
#         return self._tool_id

#     @tool_id.setter
#     def tool_id(self, value):
#         self._tool_id = value

#     def annular_velocity(self, flow_rate):
#         return flow_rate/self.annular_area()

#     def string_velocity(self, flow_rate):
#         return flow_rate/self.string_area()

#     def annular_area(self):
#         return (((self.annular_od/2)**2)-((self.annular_id/2) ** 2)) * math.pi

#     def annular_volume(self):
#         return (self.annular_area()* self.section_length).to(unit_volume)

#     def string_area(self):
#             return ((self.tool_id/2) ** 2) * math.pi

#     def string_volume(self):
#         return (self.string_area() * self.section_length).to(unit_volume)

#     def pipe_displacement_area(self):
#         return (((self.tool_od/2)**2)-((self.tool_id/2) ** 2)) * math.pi

#     def pipe_displacement_volume(self):
#         return (self.pipe_displacement_area() * self.section_length).to(unit_volume)

    # # def depth_drilled(self, depth_drilled_unit="feet") -> Depth:
        
    # #     internal_unit = "meters"
    # #     length_in_meters = self.length.to_unit(internal_unit)    
    # #     width_in_meters = self.width.to_unit(internal_unit)
    # #     height_in_meters = self.height.to_unit(internal_unit)
        
    # #     internal_value = 4 * (length_in_meters + width_in_meters + height_in_meters)
    # #     internal_quantity = Length(internal_value, internal_unit)
        
    # #     return Length(internal_quantity.to_unit(perimeter_unit), perimeter_unit)        
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


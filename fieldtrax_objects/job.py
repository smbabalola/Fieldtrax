import unittest
import sqlite3
from datetime import datetime
# from config import 
from constants import ZERO_DEPTH, internal_depth_unit

from quantity import (Diameter, Length, Depth, FlowRate, Velocity, UnitCapacity, 
                      Volume, LinearDensity, Pressure, Torque)
from pipe import Pipe, Casing, Liner, Tool, OpenHole, DrillString
from section import Section

class Job:
    def __init__(self, id: int=0, jobcenter_id: int=0, well_name:str="", country:str="", field:str="", 
                 spuddate:datetime=datetime.now(), waterdepth:Depth=ZERO_DEPTH, 
                 contractor:str="", contractorrep:str="", spud_date= None):
        self.jobid = id
        self.jobcenterid = jobcenter_id
        # self.flowrate = flowrate
        # self.pumps = []
        # self.operator = ""
        # self.operator_rep = ""
        self.well_name = well_name
        # self.rigid = ""
        self.country = country
        self.field = field
        self.contractor = contractor
        self.contractorrep =contractorrep
        self.waterdepth = waterdepth
        self.spuddate = datetime.strptime(spuddate, "%Y-%m-%d")
        self.welldata = []
        # self.DailyReports = []
        # self.jobdetails = []
        self.fluids = []
        self.joblog = []
        self.delivery_tickets = []
        self.time_sheet = None
        self.purchase_order = None
        self.service_ticket = None
        self.physical_barrier = None
        self.tally = None
        self.backload_sheet = None
        
    def set_time_sheet(self, time_sheet):
        self.time_sheet = time_sheet

    def set_purchase_order(self, purchase_order):
        self.purchase_order = purchase_order
        
    def set_service_ticket(self, service_ticket):
        self.service_ticket = service_ticket
        
    def set_physical_barrier(self, physical_barrier):
        self.physical_barrier = physical_barrier
        
    def set_tally(self, tally):
        self.tally = tally
    
    def set_backload(self, backload_sheet):
        self.backload_sheet = backload_sheet
        
    def get_job_by_id(self, job_id):
        # Assuming you have a database connection
        conn = sqlite3.connect("your_database.db")
        cursor = conn.cursor()

        # Execute a SQL query to retrieve the job with the specified ID
        cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
        job_data = cursor.fetchone()

        if job_data:
            # Create a new Job object from the retrieved data
            job = Job(job_id=job_data[0], 
                      jobcenter_id=job_data[1], 
                      well_name=job_data[2],
                      country=job_data[3],
                      field = job_data[4],
                      contractor = job_data[5],
                      contractor_rep = job_data[6],
                      water_depth = job_data[7],
                      spud_date =  job_data[8]
                      )
            return job
        else:
            return None
        # Close the database connection
        conn.close()






















    
#     def add_fluid(self, fluid):
#         self.fluids.append(fluid)
    
#     def add_casing(self, casing):
#         self.casings.append(casing)

#     def delete_casing(self, casing):
#         self.casings.remove(casing)

#     def select_casing(self, index):
#         return self.casings[index]

#     def delete_casing(self, casing):
#         self.casings.remove(casing)

#     def select_casing(self, index):
#         return self.casings[index]

#     def add_liner(self,liner):
#         self.liners.append(liner)

#     def delete_liner(self, liner):
#         self.liners.remove(liner)

#     def select_liner(self, index):
#         return self.liner[index]

#     def add_hole(self, hole):
#         self.holes.append(hole)

#     def delete_hole(self, hole):
#         self.holes.remove(hole)

#     def select_hole(self, index):
#         return self.holes.items[index]

# def calculate_hole_volume(well):
#     """Calculates the total hole volume of a well.

#     Args:
#         well (Well): The well object containing casings, liners, and open holes.

#     Returns:
#         Volume: The total hole volume.
#     """

#     total_volume = zero_volume

#     # Find the last casing
#     last_casing = None
#     for casing in well.casings:
#         if last_casing is None or casing.end_depth > last_casing.end_depth:
#             last_casing = casing
    

#     # Calculate casing volume up to the top of the last liner
#     if last_casing :
#         casing_volume = last_casing.pipe_volume()
#         top_liner_depth = max(liner.starting_depth for liner in well.liners)
#         if top_liner_depth > last_casing.starting_depth:
#             casing_volume = last_casing.pipe_volume(top_liner_depth)

#         total_volume += casing_volume

#     # Calculate liner volumes
#     for liner in well.liners:
        
#         liner_volume = liner.pipe_volume()
#         total_volume += liner_volume
#         top_liner_depth = max(liner.starting_depth for liner in well.liners)

#     # Calculate open hole volumes below liners
#     for liner in well.liners:
#         if liner.openhole:
#             total_volume += liner.openhole.Open_hole_volume(liner.end_depth)

#     return total_volume
#     def getsection(self, depth):
#         for section in self.sections:
#             if depth >= section.start_depth and depth < section.end_depth:
#                 print(f"start_depth {section.start_depth},end_depth: {section.end_depth}")
#                 return section

#     def add_section(self, section):
#         self.sections.append(section)
#         print(f"section_name: {section.section_name}, ID: {section.annular_id}, OD: {section.annular_od}, section_length: {section.section_length}")
#         print(f"Annular Volume: {section.annular_volume()}")
#         print(f"section_name: {section.section_name}, Tool ID: {section.tool_id}, OD: {section.tool_od}, tool_length: {section.section_length}")
#         print(f"Pipe Volume: {section.string_volume()}")
#         print(f"---------")

#     def create_new_section(self, outterstring, innerstring):
#         if innerstring.end_depth < outterstring.end_depth:
#             section_name = outterstring.short_name + "/" + innerstring.short_name
#             annular_od = outterstring.id
#             annular_id = innerstring.od
#             section_length = innerstring.end_depth - innerstring.start_depth
#             print(f"end depth: {innerstring.end_depth}, start Depth: {innerstring.start_depth}")
#             self.create_section(section_name,annular_od,annular_id,innerstring.start_depth, innerstring.end_depth,innerstring.od,innerstring.id)
#         else:
#             #create upper section
#             section_name = outterstring.short_name + "/" + innerstring.short_name
#             annular_od = outterstring.id
#             annular_id = innerstring.od
#             section_length = outterstring.end_depth - innerstring.start_depth
#             self.create_section(section_name,annular_od,annular_id,innerstring.start_depth,outterstring.end_depth,innerstring.od,innerstring.id)
#             #create bottom section
#             depth = innerstring.end_depth
#             print(f"Depth: {depth}")
#             mypipe = self.getoutterstring(depth)
#             if mypipe is None: return
#             section_name = mypipe.short_name +"/" +innerstring.short_name
#             annular_od = mypipe.id
#             annular_id = innerstring.od
#             section_length = innerstring.end_depth - outterstring.end_depth
#             #create upper section
#             self.create_section(section_name,annular_od,annular_id,outterstring.end_depth, innerstring.end_depth,innerstring.od,innerstring.id)

#     def create_section(self, section_name, annular_od, annular_id, start_depth, end_depth, tool_od, tool_id):
#         section = Section(section_name,annular_od,annular_id,start_depth,end_depth,tool_od,tool_id)
#         self.add_section(section)

#     # def create_calc_section(self, section_name,annular_velocity, string_velocity):
#     #     sectionhydraulics =  SectionHydraulics(section_name, annular_velocity, string_velocity)
#     #     self.add_section_hydraulics(sectionhydraulics)

#     def delete_section(self, section):
#         self.sections.remove(section)

#     def select_section(self, index):
#         return self.sections[index]

#     def add_tool(self, tool):
#         self.drillstring.append(tool)

#     def delete_tool(self, tool):
#         self.drillstring.remove(tool)

#     def select_tool(self, index):
#         return self.drillstring[index]

#     def LastCasing(self):
#         longest_casing = None
#         max_length = Length(0, "ft")
#         for casing in self.casings:
#             if casing.length.format("ft") >  max_length.format("ft"):
#                 max_length = casing.length
#                 longest_casing = casing
#         return longest_casing

#     def GetMainHole(self):
#         main_hole = None
#         for hole in self.holes:
#             if hole.main_hole == True and main_hole !=None:
#                 raise TypeError("Only one Main hole is allowed!")
#             main_hole = hole
#         return main_hole

#     def SortLiners(self):
#         # return sorted(self.liners, key=lambda x: x.end_depth)
#         sorted_liners = []
#         for liner in self.liners:
#             inserted = False
#         for i, sorted_liner in enumerate(sorted_liners):
#             if liner.end_depth < sorted_liner.end_depth:
#                 sorted_liners.insert(i, liner)
#                 inserted = True
#                 break
#         if not inserted:
#             sorted_liners.append(liner)
#         return sorted_liners

#     def SortCasings(self):
#         return sorted(self.casings, key=lambda x: x.end_depth.value)

#     def SortHoles(self):
#         return sorted(self.holes, key=lambda x: x.end_depth.value)

#     def sorttools(self):
#         return sorted(self.drillstring, key=lambda x: x.end_depth.value)

#     def createouterstrings(self):
#         casing = self.LastCasing()
#         liners = self.SortLiners()
#         mainhole = self.GetMainHole()
#         #create outerstring dictionary
#         index = 0
#         if casing:
#             index = 1
#             self.outstrings[index] = casing

#         for liner in liners:
#             index += 1
#             self.outstrings[index] = liner

#         if mainhole:
#             self.outstrings[index+1] = mainhole

#         for key in self.outstrings:
#             print(f"outstring name:{self.outstrings[key].short_name}, outstring end depth:{self.outstrings[key].end_depth}")

#     def getoutterstring(self,depth):
#         for key in self.outstrings:
#             if depth >= self.outstrings[key].start_depth and depth < self.outstrings[key].end_depth:
#                 print(f"self.outstrings[key].start_depth {self.outstrings[key].start_depth},self.outstrings[key].end_depth: {self.outstrings[key].end_depth}")
#                 return self.outstrings[key]

#     def getoutterstringtools(self,outerstring, drillstring):
#         tools = self.sorttools()
#         newtools = []
#         for tool in tools:
#             if tool.start_depth < outerstring.end_depth:
#                 newtools.append(tool)
#         return newtools

#     def createsections(self):
#         currentdepth = Depth(0, "ft")
#         section_name = ""
#         self.createouterstrings()
#         drillstring = self.sorttools()
#         #loop through tools
#         print(f"Above Bit")
#         index = 0
#         for tool in drillstring:
#             #create sections for the last casing
#             index += 1
#             print(f"index:{index}")
#             #previousdepth = currentdepth
#             # currentdepth = tool.end_depth
#             currentdepth = tool.start_depth.format("ft")
#             print(f"tool start_depth:{tool.start_depth}, tool end depth:{tool.end_depth}")
#             if currentdepth <= self.getoutterstring(currentdepth).end_depth:
#                 self.create_new_section(self.getoutterstring(currentdepth),tool)
#                 currentdepth = tool.end_depth.format("ft")
#         print(f"Below Bit")
#         print(f"--------------------------------------------------------------------")
#         casing = self.LastCasing()
#         liners = self.SortLiners()
#         mainhole = self.GetMainHole()
#         if casing.end_depth > currentdepth:
#             # print(f"In Casing below bit: casing end depth{casing.end_depth} > previous depth:{previousdepth}")
#             sectionlength = casing.end_depth
#             section_name = casing.short_name
#             self.create_section(section_name, casing.inner_diameter,zero_in, zero_ft,sectionlength,zero_in,zero_in)
#             #previousdepth = currentdepth
#             currentdepth = casing.end_depth
#         # print(f"liner w/o pipe section: Current depth: {currentdepth} > previous depth:{previousdepth}")
#         if len(liners) !=0:
#             for liner in liners:
#                 if liner.end_depth > currentdepth:
#                     # print(f"In liner below bit: liner end depth: {liner.end_depth} > previous depth: {previousdepth}, current depth:{currentdepth}")
#                     sectionlength = liner.end_depth - currentdepth
#                     section_name = liner.short_name
#                     self.create_section(section_name, liner.id,0,sectionlength, 0,0)
#                     currentdepth = liner.end_depth
#         # print(f"Hole w/o pipe section: Current depth: {currentdepth} > previous depth:{previousdepth}")
#         if mainhole != None:
#             if mainhole.end_depth > currentdepth:
#                 # print(f"In main hole below bit: mainhole end depth{mainhole.end_depth} > previous depth: {previousdepth}")
#                 sectionlength = mainhole.end_depth - currentdepth
#                 section_name = mainhole.short_name
#                 self.create_section(section_name, mainhole.id,0,sectionlength, 0,0)
#                 currentdepth = mainhole.end_depth
                        
# class TestWell(unittest.TestCase):
#     def test_fluid_movement(self):
#         pass

#     def test_well_hydraulics(self):
#         # for hydraulics in self.hydraulicsreport:
#         #     print(f"section_name: {hydraulics.section_name}")
#         #     print(f"Annular Volocity: {hydraulics.annular_velocity}")
#         #     print(f"String Volume: {hydraulics.string_velocity}")
#         #     print(f"------------------------------------------------")
#         pass

#     def test_well_sections(self):
#         #unit specification
#         well = Job()
#         #well.flow_rate = input('flow rate:')
#         # #model the wellbore geometry
#         # od = Diameter(2024, "in")
#         # id = Diameter(18, "in")
#         # csg_length = Length(1000,"ft")    
#         # well.add_casing(Casing(od, id, csg_length))
#         open_hole1 = OpenHole(inner_diameter=Diameter(24, "in"), start_depth=Depth(0, "ft"), end_depth=Depth(1000, "ft"))
#         well.open_hole = open_hole1
        

#         # od = Diameter(9.625, "in")
#         # id = Diameter(8.835, "in")
#         # csg_length = Length(6018,"ft")
        
#         # well.add_casing(Casing(od, id, csg_length))
         
#         # # #well.add_casing(Casing(16, 14, 3000))
#         # od = Diameter(7, "in")
#         # id = Diameter(6.090, "in")
#         # csg_length = Length(3571,"ft")
#         # starting_depth = (5719, "ft")    

#         # well.add_liner(Liner(od, id, csg_length, starting_depth))
#         # # #well.add_liner(Liner(5, 4.5, 13696, 14196))
#         # well.add_hole(Hole(5.875, 13696, 15400, main_hole=True))
#         # #well.add_hole(Hole(16, 0, 5000, main_hole=True))
#         # #model the drillstring
#         # well.add_tool(Tool(5, 4.276, 0, 5000))
#         # well.add_tool(Tool(5.5, 4.8, 5000, 6000))
#         # well.add_tool(Tool(5, 4.276, 6000, 10000))
#         # well.add_tool(Tool(5.5, 4.8, 10000, 13000))
#         # tool = Tool(5.5, 4.8, 13000, 15400)
#         # # tool.id = 4
#         # well.add_tool(tool)
#         #
#         # #well.add_tool(Tool(5, 3.877, 1500, 2000))
#         # #well.add_tool(Tool(5, 3.202, 2000, 3500))
#         # #well.add_tool(Tool(5.5, 4.276, 5300, 7500))
#         # # well.add_tool(Tool(5, 3.877, 500))
#         # # well.add_tool(Tool(5.5, 3.877, 500))
#         # # well.add_tool(Tool(5.5, 4.276,	400))
#         # # well.add_tool(Tool(4, 3.5,400))
#         # #well.add_tool(Tool(22, 2, 2))
#         # Calculate the hole volume
#         hole_volume = well.get_HoleVolume()
#         print("Hole volume:", hole_volume)        
        
#         # volume = zero_volume
#         # pipedispvol = zero_volume
#         # print(f"running...")
#         # well.createsections()
#         # for section in well.sections: 
#         #     volume += section.annular_volume() + section.string_volume()
#         #     pipedispvol += section.pipe_displacement_volume()
#         #     print(f"Section Name: {section.section_name}, Annular section od: {section.annular_od}, Annular Section id: {section.annular_id}, Section length {section.section_length}")
#         #     print(f"Tool od: {section.tool_od}, Tool id: {section.tool_id}")
#         #     print(f"Annular Volume: {section.annular_volume()}, String Volume: {section.string_volume()}, Pipe Displacement:{section.pipe_displacement_volume()}")
#         # print(f"Hole Volume: {volume}")
#         # print(f"Pipe Displacement Volume: {pipedispvol}")
#         #model for trajectory data
#         # well.hydraulicis_analysis()
#         # print(f"Hydraulics Analysis")
#         # print(f"-------------------")
#         # for hydraulics in well.hydraulicsreport:
#         #     print(f"section_name: {hydraulics.section_name}")
#         #     print(f"Annular Velocity: {hydraulics.annular_velocity}")
#         #     print(f"String Velocity: {hydraulics.string_velocity}")
#         #     print(f"------------------------------------------------")
# 

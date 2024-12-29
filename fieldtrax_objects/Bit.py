from quantity import (Depth, Length, Diameter, Area, Azimuth, Volume, Weight, LinearDensity, 
                      Pressure, Torque, Capacity, BarrelofOilEquivalent,BitNozzleDiameter, 
                      DLS, Density, Energy, FluidPressure, FluidVolume, Force, Mass, MudWeight,
                      PumpPressure, SaltConcentration, Stress,  Viscosity, Volume, Velocity, 
                      UnitCapacity, FlowRate, WeightonBit, WeightperLength,Temperature
)
from  constants import ZERO_BITNOZZLEDIAMETER

class Bit:
    def __init__(self):
        self.id = 0
        self.report_date = ""
        self.nozzle_size1 = ZERO_BITNOZZLEDIAMETER
        self.no_nozzles1 = ZERO_BITNOZZLEDIAMETER
        self.nozzle_size2 = ZERO_BITNOZZLEDIAMETER
        self.no_nozzles2 = ZERO_BITNOZZLEDIAMETER
        self.nozzle_size3 = ZERO_BITNOZZLEDIAMETER
        self.no_nozzles3 = ZERO_BITNOZZLEDIAMETER
        self.bit_no = ""
        self.bit_type = ""
        self.depth_in = 0
        self.depth_out = 0

# Bit calculations
    def bit_pressure_loss(self,flow_rate,mud_weight):
        return (156.5 * self.flow_rate**2 *self.mud_weight)/((self.nozzle_size1**2)+(self.nozzle_size2**2)+(self.nozzles_size3**3))

    @property
    def bit_HHP(self,surface_pressure):
        return surface_pressure* self.bit_pressure_loss/1714

    def bit_HHP_persqin(self, nozzle_size):
        return (self.bit_HHP * 1.27)/(self.nozzle_size**2)

    def bit_percent_pressure_loss(self,surface_pressure):
        return (self.bit_pressure_loss/surface_pressure)*100

    def jet_velocity(self,flow_rate):
        return (417.2 * flow_rate)/((self.nozzle_size1**2)+(self.nozzle_size2**2)+ (self.nozzle_size3**2))

    @property
    def impact_force_bit_area(self):
        return self.impact_force_bit * 1.27/self.bit.size

    def impact_force_bit(self, mud_weight, flow_rate):
        return (mud_weight*self.jet_velocity*flow_rate)/1930

    @property
    def total_flow_area(self):
        return (((self.nozzle_size1**2)+(self.nozzle_size2**2)+(self.nozzles_size3**2))/1303.8)

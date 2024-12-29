# constants.py
from quantity import (Depth, Length, Diameter, Area, Azimuth, Volume, Weight, LinearDensity, 
                      Pressure, Torque, Capacity, BarrelofOilEquivalent,BitNozzleDiameter, 
                      DLS, Density, Energy, FluidPressure, FluidVolume, Force, Mass, MudWeight,
                      PumpPressure, SaltConcentration, Stress,  Viscosity, Volume, Velocity, 
                      UnitCapacity, FlowRate, WeightonBit, WeightperLength,Temperature
)

ZERO_DEPTH = Depth(0, "ft")
ZERO_LENGTH = Length(0, "ft")
ZERO_DIAMETER = Diameter(0, "in")
ZERO_AZIMUTH = Azimuth(0, "deg")
ZERO_AREA = Area(0,"ft2")
ZERO_VOLUME = Volume(0, "bbl")
ZERO_WEIGHT = Weight(0, "kg")
ZERO_LINEARDENSITY = LinearDensity(0, "kg/m")
ZERO_PRESSURE = Pressure(0,"psi")
ZERO_TORQUE = Torque(0, "klbf.ft")
ZERO_BARRELOFOILEQUIPMENT = BarrelofOilEquivalent(0, "boe")
ZERO_BITNOZZLEDIAMETER = BitNozzleDiameter(0, "in")
ZERO_DLS = DLS(0, "deg/100ft")
ZERO_DENSITY = Density(0, "lb/gal")#
ZERO_ENERGY = Density(0,"N.m")
ZERO_FLUIDPRESSURE = FluidPressure(0, "psi")
ZERO_FLUIDVOLUME = FluidVolume(0, "bbl")
ZERO_FORCE = Force(0, "klbf")
ZERO_MASS = Mass(0, "klb")
ZERO_MUDWEIGHT = MudWeight(0, "lb/gal")
ZERO_PUMPPRESSURE = PumpPressure(0, "psi")
ZERO_SALTCONCENTRATION = SaltConcentration(0, "lb/bbl")
ZERO_STRESS = Stress(0, "psi")
ZERO_VISCOSITY = Viscosity(0, "cp")
ZERO_VOLUME =Volume(0,"bbl" )
ZERO_VELOCITY = Velocity(0, "ft/min")
ZERO_UNITCAPACITY = UnitCapacity(0,"bbl/ft")
ZERO_FLOWRATE = FlowRate(0,"gal/min")
ZERO_WEIGHTONBIT = WeightonBit(0,"klbf")
ZERO_WEIGHTPERLENGTH  = WeightperLength(0, "lb/bbl")
ZERO_TEMPERATURE = Temperature(0, "degC")

CUTTINGS_SG = Density(2.4, "SG")

internal_depth_unit ="ft"
internal_length_unit= "ft"
internal_diameter_unit ="in"
internal_azimuth_unit = "deg"
internal_area_unit = "ft2"
internal_weight_unit = "lbs"
internal_lineardensity_unit = "lb/ft"
internal_pressure_unit = "psi"
internal_torque_unit = "klbf.ft"
internal_barrelofOilequivalent_unit = "boe"
internal_bitnozzlediameter_unit = "in"
internal_DLS_unit = "deg/100ft"
internal_density_unit = "lb/gal"
internal_energy_unit = "j"
internal_fieldpressure_unit = "psi"
internal_fluidvolume_unit = "bbl"
internal_force_unit = "klbf"
internal_mass_unit = "klb"
internal_mudweight_unit = "lb/gal"
internal_pumppressure_unit = "psi"
internal_saltconcentration_unit = "lb/bbl"
internal_stress_unit = "psi"
internal_viscosity_unit = "cp"
internal_volume_unit = "bbl"
internal_velocity_unit = "ft/min"
internal_unitcapacity_unit = "bbl/ft"
internal_flowrate_unit = "gal/min"
internal_weightonbit_unit = "klbf"
internal_weightperlength = "lb/bbl"
internal_temperature_unit = "degC"
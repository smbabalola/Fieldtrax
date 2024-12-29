from quantity import Depth, Length, Viscosity, UnitCapacity, Volume,LinearDensity, Pressure,Torque, Temperature, MudWeight
import math

class Fluid():
    def __init__(self, temperature: Temperature, top_depth: Depth, bottom_depth:Depth, 
                 mud_weight: MudWeight,  fluid_volume:Volume, interval: Length,
                 r600: Viscosity=0, r300: Viscosity=0, r200: Viscosity=0,
                 r100: Viscosity=0, r6: Viscosity=0, r3: Viscosity=0,
                 gels10s: Viscosity=0, gels10m: Viscosity=0, gels30m: Viscosity=0,
                 api_fluid_loss: Volume=0, hthp_fluid_loss: Volume=0, hthp_temp: Temperature=0,
                 cake_api:Length=0, cake_hthp: Length=0, sand_content: float=0, oil_percent: float=0,
                 water_percent: float=0, solid_percent: float=0, alkanality: float=0, emulsion_stability: int=0 ):
        self.temperature = temperature
        self.top_depth = top_depth
        self.bottom_depth = bottom_depth
        self.mud_weight = mud_weight
        self.volume = fluid_volume
        self.interval = interval
        self.r600 = r600
        self.r300 = r300
        self.r200 = r200
        self.r100 = r100
        self.r6 = r6
        self.r3 = r3
        self.gel10s = gels10s
        self.gel10m = gels10m
        self.gel30m = gels30m
        self.api_fluid_loss = api_fluid_loss
        self.hthp_fluid_loss = hthp_fluid_loss
        self.hthp_temp = hthp_temp
        self.cake_apl =  cake_api
        self.cake_hthp = cake_hthp
        self.sand_content = sand_content
        self.oil_percent = oil_percent
        self.water_percent = water_percent
        self.solid_percent = solid_percent
        self.alkanality = alkanality
        self.emulsionstability = emulsion_stability

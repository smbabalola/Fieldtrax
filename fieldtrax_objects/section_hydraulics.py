
class SectionHydraulics:
    def __init__(self, section_name, annular_velocity, string_velocity, slip_velocity, critical_flow_rate):
        self._section_name = section_name
        self._annular_velocity = ureg.Quantity(annular_velocity, unit_velocity)
        self._string_velocity = ureg.Quantity(string_velocity, unit_velocity)
        self._slip_velocity =  ureg.Quantity(slip_velocity, unit_velocity)
        self._critical_annular_velocity = ureg.Quantity(critical_annular_velocity, unit_velocity)
        self._critical_flow_rate =  ureg.Quantity(critical_flow_rate, unit_flow_rate)

    @property
    def section_name(self):
        return self._section_name

    @property
    def annular_velocity(self):
        return self._annular_velocity

    @property
    def string_velocity(self):
        return self._string_velocity

    @property
    def slip_velocity(self):
        return self._slip_velocity

    @property
    def critical_annular_velocity(self):
        return self._critical_annular_velocity

    @property
    def critical_flow_rate(self):
        return self._critical_flow_rate
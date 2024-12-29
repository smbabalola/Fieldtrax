from sqlalchemy import Boolean, Column, Enum, String, Integer, ForeignKey, Float

from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class PackerType(Enum):
    INTEGRAL = "integral packer"
    NO_PACKER = "no packer"
    SECOND_TRIP = "second trip packer"

class HangerInfo(BaseDBModel):
    __tablename__ = 'hanger_infos'

    wellbore_id = Column(String(50), ForeignKey('wellbores.id'), nullable=True)
    type = Column(String(20), nullable=True)
    burst_rating = Column(Float, nullable=True)
    tensile_rating = Column(Float, nullable=True)
    hanging_capacity = Column(Float, nullable=True)
    hydraulic_setting_pressure = Column(Float, nullable=True)
    
    rotatable_run_in = Column(Boolean, nullable=True)
    hydraulic_set = Column(Boolean, nullable=True)
    rotatable_cmt = Column(Boolean, nullable=True)
    _packer_type = Column(String(25), nullable=True)
    cont_tieback_packer_req = Column(Boolean, nullable=True)
    extension_length = Column(Float, nullable=True)

    @property
    def packer_type(self):
        if self._packer_type:
            try:
                return PackerType(self._packer_type)
            except ValueError:  # Handle cases where the database has an invalid value.
                return None # Or raise an exception if you prefer
        return None

    @packer_type.setter
    def packer_type(self, value):
        if value is None:
            self._packer_type = None
        elif isinstance(value, PackerType):
            self._packer_type = value.value
        else:
            raise ValueError("Invalid packer type. Use PackerType enum values.")

    def __repr__(self):
        return f"<HangerInfo(packer_type={self.packer_type})>"

    wellbore = relationship('Wellbore', back_populates='hanger_infos')

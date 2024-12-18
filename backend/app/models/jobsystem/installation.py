from sqlalchemy import Column, String, Integer, ForeignKey, Float

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class Installation(BaseDBModel):
    __tablename__ = 'installations'

    field_id = Column(String(50), ForeignKey("fields.id"), nullable=True)
    installation_name = Column(String(25), nullable=True)
    installation_type_id = Column(String(50), ForeignKey("installation_types.id"), nullable=True)
    field_block = Column(String(50), nullable=True)
    water_depth = Column(Float, nullable=True)

    slots = relationship('Slot', back_populates='installation')
    installation_type = relationship('InstallationType', back_populates='installations')

    def __repr__(self):
        return f"<Installation: {self.installation_name}>"

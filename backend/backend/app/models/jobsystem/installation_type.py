
from sqlalchemy import Column, String

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class InstallationType(BaseDBModel):
    __tablename__ = 'installation_types'

    installation_type = Column(String(50), nullable= True)
    description = Column(String(100), nullable=True)

    installations = relationship('Installation', back_populates='installation_type')

    def __repr__(self):
        return f"<InstallationType: {self.Installation_type}>"
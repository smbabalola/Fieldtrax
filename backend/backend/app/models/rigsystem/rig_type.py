from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.base import BaseDBModel

class RigType(BaseDBModel):
    __tablename__ = "rig_types"

    rig_type_name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(500), nullable=True)

    rigs = relationship("Rig", back_populates="rig_type")

    def __repr__(self):
        return f"<RigType: {self.rig_type_name}>"
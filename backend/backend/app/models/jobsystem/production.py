from sqlalchemy import Column, String

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class Production(BaseDBModel):
    __tablename__ = 'productions'

    production_type = Column(String(30), nullable=True)
    description = Column(String(100), nullable=True)

    wells = relationship('Well', back_populates='production') 

    def __repr__(self):
        return f"<Production: {self.production_type}>"
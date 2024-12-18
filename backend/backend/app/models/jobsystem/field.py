from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class Field(BaseDBModel):
    __tablename__ = 'fields'

    field_name = Column(String(50), nullable=False)
    lease_name = Column(String(25), nullable=True)
    country = Column(String(25), nullable=True)
    state = Column(String(25), nullable=True)
    area = Column(String(25), nullable=True)
    
    #relationship
    # wells = relationship('Well', back_populates='field')

    def __repr__(self):
        return f"<Field: {self.field_name}>"
    
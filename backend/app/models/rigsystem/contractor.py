from app.models.base import Base, BaseDBModel
from sqlalchemy import Column, String, NCHAR
from sqlalchemy.orm import relationship

class Contractor(BaseDBModel):
    __tablename__ = 'contractors'

    contractor_name = Column(String(30), nullable=False)
    address_1 = Column(String(30), nullable=True)
    address_2 = Column(String(30), nullable=True)
    post_code = Column(NCHAR(15), nullable=True)
    zipcode = Column(NCHAR(15), nullable=True)
    phone_no_1 = Column(String(15), nullable=True)
    phone_no_2 = Column(String(15), nullable=True)
    state = Column(NCHAR(30), nullable=True)
    country = Column(NCHAR(30), nullable=True)

    rigs = relationship('Rig', back_populates='contractor') 

    def __repr__(self):
        return f"<Contractor: {self.contractor_name}>"
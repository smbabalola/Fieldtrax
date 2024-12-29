from sqlalchemy import Column, String, NCHAR

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class Operator(BaseDBModel):
    __tablename__ = 'operators'

    operator_name = Column(String(30), nullable=False)
    company_code = Column(NCHAR(4), nullable=False)
    account = Column(String(30), nullable=True)
    address_1 = Column(String(30), nullable=True)
    address_2 = Column(String(30), nullable=True)
    post_code = Column(NCHAR(15), nullable=True)
    zipcode = Column(NCHAR(15), nullable=True)
    phone_no_1 = Column(String(30), nullable=True)
    phone_no_2 = Column(String(30), nullable=True)
    state = Column(NCHAR(30), nullable=True)
    country = Column(NCHAR(30), nullable=True)

    jobs = relationship('Job', back_populates='operator')
    wells = relationship('Well', back_populates='operator')

    def __repr__(self):
        return f"<Operator: {self.operator_name}>"
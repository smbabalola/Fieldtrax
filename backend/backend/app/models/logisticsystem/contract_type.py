from sqlalchemy import Column, String

from app.models.base import Base, BaseDBModel

class ContractType(BaseDBModel):
    __tablename__ = 'contract_types'

    contract_type = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<ContractType: {self.contract_type}>"
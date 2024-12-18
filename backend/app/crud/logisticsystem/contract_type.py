# File: backend/app/crud/logisticssystem/crud_contract_type.py
from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.logisticssystem.contract_type import ContractType
from app.schemas.logisticssystem.contract_type import ContractTypeCreate, ContractTypeUpdate

class CRUDContractType(CRUDBase[ContractType, ContractTypeCreate, ContractTypeUpdate]):
    async def get_by_type(
        self, 
        db: Session, 
        *, 
        contract_type: str
    ) -> Optional[ContractType]:
        """Get contract type by name"""
        return db.query(ContractType).filter(
            ContractType.contract_type == contract_type
        ).first()


crud_contract_type = CRUDContractType(ContractType)


# from app.models.logisticsystem.purchase_order_item import PurchaseOrderItem
# from app.crud.base import CRUDBase

# crud_purchase_order_item = CRUDBase(PurchaseOrderItem)
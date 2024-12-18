# File: backend/app/crud/jobsystem/crud_operator.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.operator import Operator
from app.schemas.jobsystem.operator import OperatorCreate, OperatorUpdate

class CRUDOperator(CRUDBase[Operator, OperatorCreate, OperatorUpdate]):
    async def get_by_company_code(
        self, 
        db: Session, 
        *, 
        company_code: str
    ) -> Optional[Operator]:
        """Get operator by company code"""
        return db.query(Operator).filter(
            Operator.company_code == company_code
        ).first()

    async def get_by_name(
        self, 
        db: Session, 
        *, 
        operator_name: str
    ) -> Optional[Operator]:
        """Get operator by name"""
        return db.query(Operator).filter(
            Operator.operator_name == operator_name
        ).first()

crud_operator = CRUDOperator(Operator)
# from app.models.jobsystem.operator import Operator
# from app.crud.base import CRUDBase

# crud_operator = CRUDBase(Operator)
# File: backend/app/crud/rigsystem/crud_contractor.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.rigsystem.contractor import Contractor
from app.schemas.rigsystem.contractor import ContractorCreate, ContractorUpdate

class CRUDContractor(CRUDBase[Contractor, ContractorCreate, ContractorUpdate]):
    async def get_by_name(
        self, 
        db: Session, 
        *, 
        contractor_name: str
    ) -> Optional[Contractor]:
        """Get contractor by name"""
        return db.query(Contractor).filter(
            Contractor.contractor_name == contractor_name
        ).first()

    async def get_by_country(
        self,
        db: Session,
        *,
        country: str
    ) -> List[Contractor]:
        """Get contractors by country"""
        return db.query(Contractor).filter(
            Contractor.country == country
        ).all()
        
crud_contractor = CRUDContractor(Contractor)

# from app.models.rigsystem.contractor import Contractor
# from app.crud.base import CRUDBase

# crud_contractor = CRUDBase(Contractor)


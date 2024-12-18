# File: backend/app/crud/jobsystem/crud_production.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.production import Production
from app.schemas.jobsystem.production import ProductionCreate, ProductionUpdate

class CRUDProduction(CRUDBase[Production, ProductionCreate, ProductionUpdate]):
    async def get_by_type(
        self, 
        db: Session, 
        *, 
        production_type: str
    ) -> List[Production]:
        """Get all productions of a specific type"""
        return db.query(Production).filter(
            Production.production_type == production_type
        ).all()

crud_production = CRUDProduction(Production)

# File: backend/app/crud/jobsystem/production.py
# from app.models.jobsystem.production import Production
# from app.crud.base import CRUDBase

# crud_production = CRUDBase(Production)
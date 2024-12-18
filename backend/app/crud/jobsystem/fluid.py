# File: backend/app/crud/jobsystem/crud_fluid.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.fluid import Fluid
from app.schemas.jobsystem.fluid import FluidCreate, FluidUpdate

class CRUDFluid(CRUDBase[Fluid, FluidCreate, FluidUpdate]):
    async def get_by_wellbore(self, db: Session, *, wellbore_id: str) -> List[Fluid]:
        """Get all fluids for a wellbore"""
        return db.query(Fluid).filter(Fluid.wellbore_id == wellbore_id).all()

    async def get_by_type(
        self, 
        db: Session, 
        *, 
        wellbore_id: str,
        fluid_type: str
    ) -> List[Fluid]:
        """Get all fluids of a specific type for a wellbore"""
        return db.query(Fluid).filter(
            Fluid.wellbore_id == wellbore_id,
            Fluid.fluid_type == fluid_type
        ).all()

crud_fluid = CRUDFluid(Fluid)

# from app.models.jobsystem.fluid import Fluid
# from app.crud.base import CRUDBase

# crud_fluid = CRUDBase(Fluid)



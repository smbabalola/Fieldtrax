# File: backend/app/crud/jobsystem/crud_well_shape.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.crud.base import CRUDBase
from app.models.jobsystem.well_shape import WellShape
from app.schemas.jobsystem.well_shape import WellShapeCreate, WellShapeUpdate

class CRUDWellShape(CRUDBase[WellShape, WellShapeCreate, WellShapeUpdate]):
    async def get_by_shape(
        self,
        db: Session,
        *,
        well_shape: str
    ) -> Optional[WellShape]:
        """Get well shape by name"""
        try:
            shape = db.query(self.model).filter(
                self.model.well_shape == well_shape
            ).first()
            
            if not shape:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Well shape not found"
                )
            return shape
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
            
    async def get_all(
        self, 
        db: Session,
        order_by: str = "well_shape"  # Default ordering by well_shape
    ) -> List[WellShape]:
        """Get all well shapes ordered by shape name"""
        return await self.get_multi(
            db=db,
            order_by=order_by
        )
crud_well_shape = CRUDWellShape(WellShape)

# File: backend/app/crud/jobsystem/well_type.py
# from app.models.jobsystem.well_shape import WellShape
# from app.crud.base import CRUDBase

# crud_well_shape = CRUDBase(WellShape)
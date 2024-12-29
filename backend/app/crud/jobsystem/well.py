# File: app/crud/jobsystem/well.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.crud.base import CRUDBase
from app.models.jobsystem.well import Well
from app.schemas.jobsystem.well import WellCreate, WellUpdate
import logging

logger = logging.getLogger(__name__)

class CRUDWell(CRUDBase[Well, WellCreate, WellUpdate]):
    async def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Well]:
        """Get multiple wells with pagination"""
        try:
            query = db.query(self.model).order_by(self.model.created_at.desc())
            total = query.count()
            logger.info(f"Found {total} total wells")
            
            wells = query.offset(skip).limit(limit).all()
            logger.info(f"Returning {len(wells)} wells")
            return wells
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_multi: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_multi: {str(e)}", exc_info=True)
            raise

    async def get(self, db: Session, id: str) -> Optional[Well]:
        """Get a single well by ID"""
        try:
            well = db.query(self.model).filter(self.model.id == id).first()
            if well:
                logger.info(f"Found well with id {id}")
            else:
                logger.warning(f"Well with id {id} not found")
            return well
        except SQLAlchemyError as e:
            logger.error(f"Database error in get: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get: {str(e)}", exc_info=True)
            raise

    async def get_by_slot(
        self,
        db: Session,
        *,
        slot_id: str
    ) -> List[Well]:
        """Get wells by slot ID"""
        try:
            wells = db.query(self.model).filter(
                self.model.slot_id == slot_id
            ).all()
            logger.info(f"Found {len(wells)} wells for slot {slot_id}")
            return wells
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_slot: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_by_slot: {str(e)}", exc_info=True)
            raise

    async def get_by_name(
        self,
        db: Session,
        *,
        well_name: str
    ) -> Optional[Well]:
        """Get well by name"""
        try:
            well = db.query(self.model).filter(
                self.model.well_name == well_name
            ).first()
            if well:
                logger.info(f"Found well with name {well_name}")
            else:
                logger.warning(f"Well with name {well_name} not found")
            return well
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_name: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_by_name: {str(e)}", exc_info=True)
            raise
        
    async def get_wells_by_operator_id(
        self, 
        db: Session, 
        *, 
        operator_id: int
        ) -> List[Well]:
        return db.query(Well).filter(Well.operator_id == operator_id).all()

crud_well = CRUDWell(Well)
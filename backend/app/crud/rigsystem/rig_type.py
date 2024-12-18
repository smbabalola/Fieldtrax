# File: backend/app/crud/wellsystem/rig_type.py
from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from uuid import uuid4

from app.models.rigsystem.rig_type import RigType
from app.schemas.rigsystem.rig_type import RigTypeCreate, RigTypeUpdate

class CRUDRigType:
    async def create(self, db: Session, *, obj_in: RigTypeCreate) -> RigType:
        """Create a new rig type"""
        db_obj = RigType(
            id=f"RT{str(uuid4())[:8].upper()}",
            rig_type_name=obj_in.rig_type_name,
            description=obj_in.description,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def get(self, db: Session, id: str) -> Optional[RigType]:
        """Get a rig type by ID"""
        return db.query(RigType).filter(RigType.id == id).first()

    async def get_by_name(self, db: Session, name: str) -> Optional[RigType]:
        """Get a rig type by name"""
        return db.query(RigType).filter(RigType.rig_type_name == name).first()

    async def get_all(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[RigType]:
        """Get all rig types with pagination"""
        return db.query(RigType).order_by(RigType.id).offset(skip).limit(limit).all()

    async def update(
        self,
        db: Session,
        *,
        db_obj: RigType,
        obj_in: Union[RigTypeUpdate, Dict[str, Any]]
    ) -> RigType:
        """Update a rig type"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def delete(self, db: Session, *, id: str) -> bool:
        """Delete a rig type"""
        try:
            obj = db.query(RigType).get(id)
            if not obj:
                return False
            db.delete(obj)
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

    async def multi_delete(self, db: Session, *, ids: List[str]) -> bool:
        """Delete multiple rig types"""
        try:
            db.query(RigType).filter(RigType.id.in_(ids)).delete(synchronize_session=False)
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

crud_rig_type = CRUDRigType()

# from app.models.rigsystem.rig_type import RigType
# from app.crud.base import CRUDBase

# crud_rig_type = CRUDBase(RigType)
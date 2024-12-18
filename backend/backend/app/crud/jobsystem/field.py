# File: backend/app/crud/jobsystem/crud_field.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.field import Field
from app.schemas.jobsystem.field import FieldCreate, FieldUpdate

class CRUDField(CRUDBase[Field, FieldCreate, FieldUpdate]):
    async def get_by_name(self, db: Session, *, field_name: str) -> Optional[Field]:
        """Get field by name"""
        return db.query(Field).filter(Field.field_name == field_name).first()

    async def get_fields_by_country(self, db: Session, *, country: str) -> List[Field]:
        """Get all fields in a country"""
        return db.query(Field).filter(Field.country == country).all()

    async def get_fields_by_area(self, db: Session, *, area: str) -> List[Field]:
        """Get all fields in an area"""
        return db.query(Field).filter(Field.area == area).all()

crud_field = CRUDField(Field)

# from app.models.jobsystem.field import Field
# from app.crud.base import CRUDBase

# crud_field = CRUDBase(Field)
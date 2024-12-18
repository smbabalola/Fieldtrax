# File: backend/app/crud/jobsystem/crud_installation.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.installation import Installation
from app.schemas.jobsystem.installation import InstallationCreate, InstallationUpdate

class CRUDInstallation(CRUDBase[Installation, InstallationCreate, InstallationUpdate]):
    async def get_by_field(
        self, 
        db: Session, 
        *, 
        field_id: str
    ) -> List[Installation]:
        """Get all installations in a field"""
        return db.query(Installation).filter(
            Installation.field_id == field_id
        ).all()

    async def get_by_name(
        self, 
        db: Session, 
        *, 
        installation_name: str
    ) -> Optional[Installation]:
        """Get installation by name"""
        return db.query(Installation).filter(
            Installation.installation_name == installation_name
        ).first()

    async def get_by_type(
        self, 
        db: Session, 
        *, 
        installation_type_id: str
    ) -> List[Installation]:
        """Get installations by type"""
        return db.query(Installation).filter(
            Installation.installation_type_id == installation_type_id
        ).all()

crud_installation = CRUDInstallation(Installation)

# from app.models.jobsystem.installation import Installation
# from app.crud.base import CRUDBase

# crud_installation = CRUDBase(Installation)
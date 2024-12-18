# File: backend/app/crud/jobsystem/crud_installation_type.py
from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.installation_type import InstallationType
from app.schemas.jobsystem.installation_type import (
    InstallationTypeCreate, 
    InstallationTypeUpdate
)

class CRUDInstallationType(CRUDBase[InstallationType, InstallationTypeCreate, InstallationTypeUpdate]):
    async def get_by_type(
        self, 
        db: Session, 
        *, 
        installation_type: str
    ) -> Optional[InstallationType]:
        """Get installation type by name"""
        return db.query(InstallationType).filter(
            InstallationType.installation_type == installation_type
        ).first()
        
crud_installation_type = CRUDInstallationType(InstallationType)

# from app.models.jobsystem.installation_type import InstallationType
# from app.crud.base import CRUDBase

# crud_installation_type = CRUDBase(InstallationType)
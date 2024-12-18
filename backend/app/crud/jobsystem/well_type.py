# File: backend/app/crud/jobsystem/well_type.py
from app.models.jobsystem.well_type import WellType
from app.crud.base import CRUDBase

crud_well_type = CRUDBase(WellType)

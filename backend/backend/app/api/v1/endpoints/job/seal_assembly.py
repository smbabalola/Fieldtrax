# File: backend/app/api/v1/endpoints/wellbore/seal_assembly.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.seal_assembly import crud_seal_assembly
from app.schemas.jobsystem.seal_assembly import (
    SealAssemblyResponse as SealAssembly, SealAssemblyCreate, SealAssemblyUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=SealAssembly)
async def create_seal_assembly(
    *,
    db: Session = Depends(get_db),
    assembly_in: SealAssemblyCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new seal assembly"""
    return await crud_seal_assembly.create(db=db, obj_in=assembly_in)

@router.get("/wellbore/{wellbore_id}", response_model=List[SealAssembly])
async def get_assemblies_by_wellbore(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all seal assemblies for a wellbore"""
    return await crud_seal_assembly.get_by_wellbore(db=db, wellbore_id=wellbore_id)

@router.put("/{assembly_id}", response_model=SealAssembly)
async def update_seal_assembly(
    *,
    db: Session = Depends(get_db),
    assembly_id: str,
    assembly_in: SealAssemblyUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update seal assembly"""
    assembly = await crud_seal_assembly.get(db=db, id=assembly_id)
    if not assembly:
        raise HTTPException(status_code=404, detail="Seal assembly not found")
    return await crud_seal_assembly.update(db=db, db_obj=assembly, obj_in=assembly_in)

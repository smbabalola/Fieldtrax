# File: backend/app/api/v1/endpoints/rig/contractor.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.rigsystem.contractor import crud_contractor
from app.schemas.rigsystem.contractor import (
    ContractorResponse as Contractor, ContractorCreate, ContractorUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User    

router = APIRouter()

@router.post("/", response_model=Contractor)
async def create_contractor(
    contractor_in: ContractorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new contractor"""
    return await crud_contractor.create(db=db, obj_in=contractor_in)

@router.get("/name/{contractor_name}", response_model=Contractor)
async def get_contractor_by_name(
    contractor_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get contractor by name"""
    contractor = await crud_contractor.get_by_name(db=db, contractor_name=contractor_name)
    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")
    return contractor

@router.get("/country/{country}", response_model=List[Contractor])
async def get_contractors_by_country(
    country: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get contractors by country"""
    return await crud_contractor.get_by_country(db=db, country=country)

@router.put("/{contractor_id}", response_model=Contractor)
async def update_contractor(
    contractor_id: str,
    contractor_in: ContractorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update contractor"""
    contractor = await crud_contractor.get(db=db, id=contractor_id)
    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")
    return await crud_contractor.update(db=db, db_obj=contractor, obj_in=contractor_in)

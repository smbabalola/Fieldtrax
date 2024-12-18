# File: backend/app/api/v1/endpoints/job/contract_type.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.contract_type import crud_contract_type
from app.schemas.jobsystem.contract_type import (
    ContractTypeResponse as ContractType, ContractTypeCreate, ContractTypeUpdate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=ContractType)
async def create_contract_type(
    contract_type_in: ContractTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new contract type"""
    return await crud_contract_type.create(db=db, obj_in=contract_type_in)

@router.get("/type/{contract_type}", response_model=ContractType)
async def get_contract_type(
    contract_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get contract type by name"""
    contract = await crud_contract_type.get_by_type(db=db, contract_type=contract_type)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract type not found")
    return contract

@router.put("/{type_id}", response_model=ContractType)
async def update_contract_type(
    type_id: str,
    contract_type_in: ContractTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update contract type"""
    contract_type = await crud_contract_type.get(db=db, id=type_id)
    if not contract_type:
        raise HTTPException(status_code=404, detail="Contract type not found")
    return await crud_contract_type.update(db=db, db_obj=contract_type, obj_in=contract_type_in)




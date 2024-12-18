# File: backend/app/api/v1/endpoints/operations/operator.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.operator import crud_operator
from app.schemas.jobsystem.operator import (OperatorResponse as Operator, 
                                            OperatorCreate, OperatorUpdate)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=Operator)
async def create_operator(
    *,
    db: Session = Depends(get_db),
    operator_in: OperatorCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new operator"""
    return await crud_operator.create(db=db, obj_in=operator_in)

@router.get("/code/{company_code}", response_model=Operator)
async def get_operator_by_code(
    company_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get operator by company code"""
    operator = await crud_operator.get_by_company_code(db=db, company_code=company_code)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return operator

@router.get("/name/{operator_name}", response_model=Operator)
async def get_operator_by_name(
    operator_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get operator by name"""
    operator = await crud_operator.get_by_name(db=db, operator_name=operator_name)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return operator

@router.put("/{operator_id}", response_model=Operator)
async def update_operator(
    *,
    db: Session = Depends(get_db),
    operator_id: str,
    operator_in: OperatorUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update operator"""
    operator = await crud_operator.get(db=db, id=operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return await crud_operator.update(db=db, db_obj=operator, obj_in=operator_in)

# In operator.py
@router.get("/", response_model=List[Operator])
async def get_operators(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get all operators"""
    return await crud_operator.get_multi(db=db, skip=skip, limit=limit)

# File: backend/app/api/v1/endpoints/operations/production.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.production import crud_production
from app.schemas.jobsystem.production import (ProductionResponse as Production, 
                                              ProductionCreate, ProductionUpdate)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=Production)
async def create_production(
    *,
    db: Session = Depends(get_db),
    production_in: ProductionCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new production record"""
    return await crud_production.create(db=db, obj_in=production_in)

@router.get("/type/{production_type}", response_model=List[Production])
async def get_production_by_type(
    production_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all productions of a specific type"""
    return await crud_production.get_by_type(db=db, type_value=production_type, type_field="production_type")

@router.put("/{production_id}", response_model=Production)
async def update_production(
    *,
    db: Session = Depends(get_db),
    production_id: str,
    production_in: ProductionUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update production record"""
    production = await crud_production.get(db=db, id=production_id)
    if not production:
        raise HTTPException(status_code=404, detail="Production record not found")
    return await crud_production.update(db=db, db_obj=production, obj_in=production_in)
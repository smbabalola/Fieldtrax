
# File: backend/app/api/api_v1/endpoints/rig/rig.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.rigsystem.rig import crud_rig
from app.schemas.rigsystem.rig import RigResponse, RigCreate, RigUpdate
from app.core.deps import get_db

router = APIRouter()

@router.post("/", response_model=RigResponse)
async def create_rig(
    rig_in: RigCreate,
    db: Session = Depends(get_db)
):
    """Create new rig"""
    return await crud_rig.create(db=db, obj_in=rig_in)

@router.get("/", response_model=List[RigResponse])
async def read_rigs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all rigs"""
    return await crud_rig.get_multi(db, skip=skip, limit=limit)

@router.get("/active", response_model=List[RigResponse])
async def read_active_rigs(
    db: Session = Depends(get_db)
):
    """Get active rigs"""
    return await crud_rig.get_active_rigs(db=db)

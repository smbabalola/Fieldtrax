# File: backend/app/api/v1/endpoints/tally/tally.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.tally import crud_tally
from app.schemas.jobsystem.tally import TallyResponse as Tally, TallyCreate, TallyUpdate
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=Tally)
async def create_tally(
    *,
    db: Session = Depends(get_db),
    tally_in: TallyCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new tally"""
    return await crud_tally.create(db=db, obj_in=tally_in)

@router.get("/{tally_id}", response_model=Tally)
async def get_tally(
    tally_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tally by ID"""
    tally = await crud_tally.get(db=db, id=tally_id)
    if not tally:
        raise HTTPException(status_code=404, detail="Tally not found")
    return tally

@router.put("/{tally_id}", response_model=Tally)
async def update_tally(
    *,
    db: Session = Depends(get_db),
    tally_id: str,
    tally_in: TallyUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update tally"""
    tally = await crud_tally.get(db=db, id=tally_id)
    if not tally:
        raise HTTPException(status_code=404, detail="Tally not found")
    return await crud_tally.update(db=db, db_obj=tally, obj_in=tally_in)
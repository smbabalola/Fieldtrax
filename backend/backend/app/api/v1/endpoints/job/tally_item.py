# File: backend/app/api/v1/endpoints/tally/tally_item.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.tally_item import crud_tally_item
from app.schemas.jobsystem.tally_item import TallyItemResponse as TallyItem, TallyItemCreate, TallyItemUpdate
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=TallyItem)
async def create_tally_item(
    *,
    db: Session = Depends(get_db),
    item_in: TallyItemCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new tally item"""
    return await crud_tally_item.create(db=db, obj_in=item_in)

@router.get("/tally/{tally_id}", response_model=List[TallyItem])
async def get_items_by_tally(
    tally_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all items for a tally"""
    return await crud_tally_item.get_by_tally(db=db, tally_id=tally_id)

@router.get("/serial/{serial_number}", response_model=TallyItem)
async def get_item_by_serial(
    serial_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get item by serial number"""
    item = await crud_tally_item.get_by_serial_number(db=db, serial_number=serial_number)
    if not item:
        raise HTTPException(status_code=404, detail="Tally item not found")
    return item

@router.get("/tally/{tally_id}/total-length")
async def calculate_total_length(
    tally_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate total length of tally items"""
    total_length = await crud_tally_item.calculate_total_length(db=db, tally_id=tally_id)
    return {"total_length": total_length}

@router.put("/{item_id}", response_model=TallyItem)
async def update_tally_item(
    *,
    db: Session = Depends(get_db),
    item_id: str,
    item_in: TallyItemUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update tally item"""
    item = await crud_tally_item.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Tally item not found")
    return await crud_tally_item.update(db=db, db_obj=item, obj_in=item_in)
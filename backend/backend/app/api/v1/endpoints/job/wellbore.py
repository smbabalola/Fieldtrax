# File: backend/app/api/v1/endpoints/wellbore/wellbore.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.crud.jobsystem.wellbore import crud_wellbore
from app.schemas.jobsystem.wellbore import WellboreResponse as Wellbore, WellboreCreate, WellboreUpdate
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=Wellbore)
async def create_wellbore(
    *,
    db: Session = Depends(get_db),
    wellbore_in: WellboreCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new wellbore"""
    return await crud_wellbore.create(db=db, obj_in=wellbore_in)

@router.get("/", response_model=List[Wellbore])
async def get_all_wellbores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all wellbores with pagination"""
    return await crud_wellbore.get_multi(db=db, skip=skip, limit=limit)

@router.get("/active", response_model=List[Wellbore])
async def get_active_wellbores(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all active wellbores"""
    return await crud_wellbore.get_active_wellbores(db=db)

@router.get("/planned", response_model=List[Wellbore])
async def get_planned_wellbores(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get planned wellbores"""
    return await crud_wellbore.get_planned_wellbores(db=db)

@router.get("/completed", response_model=List[Wellbore])
async def get_completed_wellbores(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get completed wellbores"""
    return await crud_wellbore.get_completed_wellbores(db=db)

@router.get("/well/{well_id}", response_model=List[Wellbore])
async def get_wellbores_by_well(
    well_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all wellbores for a well"""
    return await crud_wellbore.get_by_well(db=db, well_id=well_id)

@router.get("/{wellbore_id}", response_model=Wellbore)
async def get_wellbore(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get wellbore by ID"""
    wellbore = await crud_wellbore.get(db=db, id=wellbore_id)
    if not wellbore:
        raise HTTPException(status_code=404, detail="Wellbore not found")
    return wellbore

@router.get("/{wellbore_id}/summary")
async def get_wellbore_summary(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive wellbore summary"""
    summary = await crud_wellbore.get_wellbore_summary(db=db, wellbore_id=wellbore_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Wellbore not found")
    return summary

@router.put("/{wellbore_id}", response_model=Wellbore)
async def update_wellbore(
    *,
    db: Session = Depends(get_db),
    wellbore_id: str,
    wellbore_in: WellboreUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update wellbore"""
    wellbore = await crud_wellbore.get(db=db, id=wellbore_id)
    if not wellbore:
        raise HTTPException(status_code=404, detail="Wellbore not found")
    return await crud_wellbore.update(db=db, db_obj=wellbore, obj_in=wellbore_in)

@router.get("/date-range", response_model=List[Wellbore])
async def get_wellbores_by_date(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get wellbores within date range"""
    return await crud_wellbore.get_by_date_range(
        db=db,
        start_date=start_date,
        end_date=end_date
    )

@router.post("/{wellbore_id}/costs")
async def calculate_wellbore_costs(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate actual vs planned costs for wellbore"""
    costs = await crud_wellbore.calculate_costs(db=db, wellbore_id=wellbore_id)
    if not costs:
        raise HTTPException(status_code=404, detail="Wellbore not found")
    return costs
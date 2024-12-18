# File: backend/app/api/v1/endpoints/wellbore/fluid.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.jobsystem.fluid import crud_fluid
from app.schemas.jobsystem.fluid import FluidResponse as Fluid, FluidCreate, FluidUpdate
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=Fluid)
async def create_fluid(
    fluid_in: FluidCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new fluid"""
    return await crud_fluid.create(db=db, obj_in=fluid_in)

@router.get("/wellbore/{wellbore_id}", response_model=List[Fluid])
async def get_fluids_by_wellbore(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all fluids for a wellbore"""
    return await crud_fluid.get_by_wellbore(db=db, wellbore_id=wellbore_id)

@router.get("/wellbore/{wellbore_id}/type/{fluid_type}", response_model=List[Fluid])
async def get_fluids_by_type(
    wellbore_id: str,
    fluid_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get fluids by type for a wellbore"""
    return await crud_fluid.get_by_type(
        db=db,
        wellbore_id=wellbore_id,
        fluid_type=fluid_type
    )

@router.put("/{fluid_id}", response_model=Fluid)
async def update_fluid(
    fluid_id: str,
    fluid_in: FluidUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update fluid"""
    fluid = await crud_fluid.get(db=db, id=fluid_id)
    if not fluid:
        raise HTTPException(status_code=404, detail="Fluid not found")
    return await crud_fluid.update(db=db, db_obj=fluid, obj_in=fluid_in)

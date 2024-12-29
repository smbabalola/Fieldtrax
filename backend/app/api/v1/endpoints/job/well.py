# File: app/api/v1/endpoints/job/well.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_active_user
from app.crud.jobsystem.well import crud_well
from app.schemas.jobsystem.well import WellCreate, WellUpdate, WellResponse  # Changed from wellsystem to jobsystem
from app.models.authsystem.user import User
from app.crud.jobsystem.slot import crud_slot  # Added for slot validation

router = APIRouter()

@router.post("/", response_model=WellResponse, status_code=status.HTTP_201_CREATED)
async def create_well(
    *,
    well_in: WellCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create new well"""
    try:
        # Validate slot exists
        slot = await crud_slot.get(db=db, id=str(well_in.slot_id))
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Slot with id {well_in.slot_id} not found"
            )
            
        return await crud_well.create(db=db, obj_in=well_in)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[WellResponse])
async def read_wells(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all wells"""
    try:
        return await crud_well.get_multi(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/slot/{slot_id}", response_model=List[WellResponse])
async def read_wells_by_slot(
    slot_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get wells by slot ID"""
    try:
        # Validate slot exists
        slot = await crud_slot.get(db=db, id=slot_id)
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Slot with id {slot_id} not found"
            )
            
        wells = await crud_well.get_by_slot(db=db, slot_id=slot_id)
        return wells
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{well_id}", response_model=WellResponse)
async def read_well(
    well_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get well by ID"""
    try:
        well = await crud_well.get(db=db, id=well_id)
        if not well:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Well not found"
            )
        return well
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{well_id}", response_model=WellResponse)
async def update_well(
    *,
    well_id: str,
    well_in: WellUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update well"""
    try:
        well = await crud_well.get(db=db, id=well_id)
        if not well:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Well not found"
            )
            
        # Validate slot_id if it's being updated
        if well_in.slot_id:
            slot = await crud_slot.get(db=db, id=str(well_in.slot_id))
            if not slot:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Slot with id {well_in.slot_id} not found"
                )
                
        return await crud_well.update(db=db, db_obj=well, obj_in=well_in)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/operator/{operator_id}", response_model=List[WellResponse])
async def get_wells_by_operator(
    operator_id: str, # Or int, depending on your operator_id type
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # Optional authentication
):
    """
    Retrieve wells associated with a specific operator.
    """
    try:
        #Attempt to convert the operator_id to an integer
        pass
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid operator ID. Must be an integer.")

    wells = await crud_well.get_wells_by_operator_id(db=db, operator_id=operator_id)

    if not wells:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No wells found for operator ID: {operator_id}")

    return wells

@router.delete("/{well_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_well(
    *,
    well_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete well"""
    try:
        well = await crud_well.get(db=db, id=well_id)
        if not well:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Well not found"
            )
        await crud_well.remove(db=db, id=well_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    await crud_well.remove(db=db, id=well_id)
# File: backend/app/api/v1/endpoints/well/rig_type.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import JSONResponse

from app.core.deps import get_db, get_current_user
from app.crud.rigsystem.rig_type import crud_rig_type
from app.schemas.rigsystem.rig_type import (
    RigTypeCreate,
    RigTypeUpdate,
    RigTypeResponse
)
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=RigTypeResponse)
async def create_rig_type(
    *,
    rig_type_in: RigTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> RigTypeResponse:
    """
    Create new rig type.
    """
    rig_type = await crud_rig_type.get_by_name(db=db, name=rig_type_in.rig_type_name)
    if rig_type:
        raise HTTPException(
            status_code=400,
            detail="Rig type with this name already exists"
        )
    return await crud_rig_type.create(db=db, obj_in=rig_type_in)

@router.get("/{rig_type_id}", response_model=RigTypeResponse)
async def get_rig_type(
    rig_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> RigTypeResponse:
    """
    Get rig type by ID.
    """
    rig_type = await crud_rig_type.get(db=db, id=rig_type_id)
    if not rig_type:
        raise HTTPException(
            status_code=404,
            detail="Rig type not found"
        )
    return rig_type

@router.get("/", response_model=List[RigTypeResponse])
async def get_rig_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1)
) -> List[RigTypeResponse]:
    """
    Get all rig types with pagination.
    """
    return await crud_rig_type.get_all(db=db, skip=skip, limit=limit)

@router.put("/{rig_type_id}", response_model=RigTypeResponse)
async def update_rig_type(
    *,
    rig_type_id: str,
    rig_type_in: RigTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> RigTypeResponse:
    """
    Update a rig type.
    """
    rig_type = await crud_rig_type.get(db=db, id=rig_type_id)
    if not rig_type:
        raise HTTPException(
            status_code=404,
            detail="Rig type not found"
        )
    
    if rig_type_in.rig_type_name:
        existing_rig_type = await crud_rig_type.get_by_name(db=db, name=rig_type_in.rig_type_name)
        if existing_rig_type and existing_rig_type.id != rig_type_id:
            raise HTTPException(
                status_code=400,
                detail="Rig type with this name already exists"
            )
    
    return await crud_rig_type.update(db=db, db_obj=rig_type, obj_in=rig_type_in)

@router.delete("/{rig_type_id}")
async def delete_rig_type(
    rig_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> JSONResponse:
    """
    Delete a rig type.
    """
    rig_type = await crud_rig_type.get(db=db, id=rig_type_id)
    if not rig_type:
        raise HTTPException(
            status_code=404,
            detail="Rig type not found"
        )
    
    success = await crud_rig_type.delete(db=db, id=rig_type_id)
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Error deleting rig type"
        )
    
    return JSONResponse(
        content={"message": "Rig type deleted successfully"},
        status_code=200
    )

@router.delete("/")
async def delete_multiple_rig_types(
    ids: List[str],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> JSONResponse:
    """
    Delete multiple rig types.
    """
    success = await crud_rig_type.multi_delete(db=db, ids=ids)
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Error deleting rig types"
        )
    
    return JSONResponse(
        content={"message": "Rig types deleted successfully"},
        status_code=200
    )
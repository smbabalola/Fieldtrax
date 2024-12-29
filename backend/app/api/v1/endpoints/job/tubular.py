from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union

from app.crud.jobsystem.tubular import crud_casing, crud_liner, crud_drillstring, crud_tubular
from app.schemas.jobsystem.tubular import (
    CasingCreate,
    CasingUpdate,
    CasingResponse,
    LinerCreate,
    LinerUpdate,
    LinerResponse,
    DrillstringCreate,
    DrillstringUpdate,
    DrillstringResponse,
    TubularCreate,
    TubularUpdate,
    TubularResponse,
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

# Generic Tubular Endpoints
@router.post("/", response_model=TubularResponse, status_code=status.HTTP_201_CREATED)
async def create_tubular(
    tubular_in: TubularCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new tubular."""
    return crud_tubular.create(db=db, obj_in=tubular_in)

@router.get("/{tubular_id}", response_model=TubularResponse)
async def get_tubular(
    tubular_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get tubular by ID."""
    tubular = await crud_tubular.get(db=db, id=tubular_id)
    if not tubular:
        raise HTTPException(status_code=404, detail="Tubular not found")
    return tubular

@router.put("/{tubular_id}", response_model=TubularResponse)
async def update_tubular(
    tubular_id: int,
    tubular_in: TubularUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update tubular"""
    tubular = await crud_tubular.get(db=db, id=tubular_id)
    if not tubular:
        raise HTTPException(status_code=404, detail="Tubular not found")
    return crud_tubular.update(db=db, db_obj=tubular, obj_in=tubular_in)

@router.delete("/{tubular_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tubular(
    tubular_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a tubular."""
    tubular = await crud_tubular.get(db=db, id=tubular_id)
    if not tubular:
        raise HTTPException(status_code=404, detail="Tubular not found")
    crud_tubular.remove(db=db, id=tubular_id)
    return

@router.get("/type/{tubulartype_id}", response_model=List[Union[TubularResponse, CasingResponse, LinerResponse, DrillstringResponse]])
async def get_tubulars_by_type(
    tubulartype_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tubulars by type"""
    tubulars = await crud_tubular.get_by_type(db=db, tubulartype_id=tubulartype_id)
    if tubulartype_id == "casing":
        return [CasingResponse(**tubular.__dict__) for tubular in tubulars]
    elif tubulartype_id == "liner":
        return [LinerResponse(**tubular.__dict__) for tubular in tubulars]
    elif tubulartype_id == "drillstring":
        return [DrillstringResponse(**tubular.__dict__) for tubular in tubulars]
    else:
        return [TubularResponse(**tubular.__dict__) for tubular in tubulars]  # Return generic Tubular for unsupported types

# ... (Casing, Liner, Drillstring endpoints as before)

# Casing Endpoints
@router.post("/casing/", response_model=CasingResponse, status_code=status.HTTP_201_CREATED)
async def create_casing(casing_in: CasingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_casing.create(db=db, obj_in=casing_in)

@router.get("/casing/{casing_id}", response_model=CasingResponse)
async def get_casing(casing_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    casing = await crud_casing.get(db=db, id=casing_id)
    if not casing:
        raise HTTPException(status_code=404, detail="Casing not found")
    return casing

@router.put("/casing/{casing_id}", response_model=CasingResponse)
async def update_casing(casing_id: int, casing_in: CasingUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    casing = await crud_casing.get(db=db, id=casing_id)
    if not casing:
        raise HTTPException(status_code=404, detail="Casing not found")
    return crud_casing.update(db=db, db_obj=casing, obj_in=casing_in)

@router.delete("/casing/{casing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_casing(casing_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    casing = await crud_casing.get(db=db, id=casing_id)
    if not casing:
        raise HTTPException(status_code=404, detail="Casing not found")
    crud_casing.remove(db=db, id=casing_id)
    return

@router.get("/casing/cement-top-range", response_model=List[CasingResponse])
async def get_casings_by_cement_top_range(min_top: float, max_top: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud_casing.get_by_cement_top_range(db=db, min_top=min_top, max_top=max_top)

# Liner Endpoints
@router.post("/liner/", response_model=LinerResponse, status_code=status.HTTP_201_CREATED)
async def create_liner(liner_in: LinerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_liner.create(db=db, obj_in=liner_in)

@router.get("/liner/{liner_id}", response_model=LinerResponse)
async def get_liner(liner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    liner = await crud_liner.get(db=db, id=liner_id)
    if not liner:
        raise HTTPException(status_code=404, detail="Liner not found")
    return liner

@router.put("/liner/{liner_id}", response_model=LinerResponse)
async def update_liner(liner_id: int, liner_in: LinerUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    liner = await crud_liner.get(db=db, id=liner_id)
    if not liner:
        raise HTTPException(status_code=404, detail="Liner not found")
    return crud_liner.update(db=db, db_obj=liner, obj_in=liner_in)

@router.delete("/liner/{liner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_liner(liner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    liner = await crud_liner.get(db=db, id=liner_id)
    if not liner:
        raise HTTPException(status_code=404, detail="Liner not found")
    crud_liner.remove(db=db, id=liner_id)
    return

@router.get("/liner/overlap-range", response_model=List[LinerResponse])
async def get_liners_by_overlap_range(
    min_overlap: float,
    max_overlap: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get liners within overlap range"""
    return await crud_liner.get_by_overlap_range(db=db, min_overlap=min_overlap, max_overlap=max_overlap)

# Drillstring Endpoints
@router.post("/drillstring/", response_model=DrillstringResponse, status_code=status.HTTP_201_CREATED)
async def create_drillstring(
    drillstring_in: DrillstringCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_drillstring.create(db=db, obj_in=drillstring_in)

@router.get("/drillstring/{drillstring_id}", response_model=DrillstringResponse)
async def get_drillstring(
    drillstring_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    drillstring = await crud_drillstring.get(db=db, id=drillstring_id)
    if not drillstring:
        raise HTTPException(status_code=404, detail="Drillstring not found")
    return drillstring

@router.put("/drillstring/{drillstring_id}", response_model=DrillstringResponse)
async def update_drillstring(
    drillstring_id: int,
    drillstring_in: DrillstringUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    drillstring = await crud_drillstring.get(db=db, id=drillstring_id)
    if not drillstring:
        raise HTTPException(status_code=404, detail="Drillstring not found")
    return crud_drillstring.update(db=db, db_obj=drillstring, obj_in=drillstring_in)

@router.delete("/drillstring/{drillstring_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drillstring(
    drillstring_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    drillstring = await crud_drillstring.get(db=db, id=drillstring_id)
    if not drillstring:
        raise HTTPException(status_code=404, detail="Drillstring not found")
    crud_drillstring.remove(db=db, id=drillstring_id)
    return

@router.get("/drillstring/component-type/{component_type}", response_model=List[DrillstringResponse])
async def get_drillstrings_by_component_type(
    component_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get drillstrings by component type"""
    return await crud_drillstring.get_by_component_type(db=db, component_type=component_type)
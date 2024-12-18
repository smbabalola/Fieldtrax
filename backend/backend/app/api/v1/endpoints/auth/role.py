# api/v1/endpoints/role.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.security import get_current_user
from app.api import deps
from app.crud import crud_role
from app.models.authsystem.user import User
from app.schemas.role import Role, RoleCreate, RoleUpdate

router = APIRouter()

@router.post("/", response_model=Role)
def create_role(
    role: RoleCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    return crud_role.create(db, obj_in=role)

@router.get("/", response_model=List[Role])
def read_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return crud_role.get_multi(db, skip=skip, limit=limit)

@router.put("/{role_id}", response_model=Role)
def update_role(
    role_id: str,
    role: RoleUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    db_role = crud_role.get(db, id=role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return crud_role.update(db, db_obj=db_role, obj_in=role)

@router.delete("/{role_id}")
def delete_role(
    role_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    db_role = crud_role.get(db, id=role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    crud_role.remove(db, id=role_id)
    return {"message": "Role deleted successfully"}

# Permissions endpoints
@router.post("/{role_id}/permissions/{permission_id}")
def add_permission_to_role(
    role_id: str,
    permission_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    return crud_role.add_permission(db, role_id=role_id, permission_id=permission_id)

@router.delete("/{role_id}/permissions/{permission_id}")
def remove_permission_from_role(
    role_id: str,
    permission_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    return crud_role.remove_permission(db, role_id=role_id, permission_id=permission_id)

# User-Role management endpoints
@router.post("/users/{user_id}/roles/{role_id}")
def assign_role_to_user(
    user_id: str,
    role_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    return crud_role.assign_to_user(db, user_id=user_id, role_id=role_id)

@router.delete("/users/{user_id}/roles/{role_id}")
def remove_role_from_user(
    user_id: str,
    role_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    return crud_role.remove_from_user(db, user_id=user_id, role_id=role_id)
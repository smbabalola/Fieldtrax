# Permissions endpoints
from fastapi import APIRouter, Depends
from pytest import Session
from app.api import deps
from documentation.schema import User
from app.crud import crud_role

router = APIRouter()
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

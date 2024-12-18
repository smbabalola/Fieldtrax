
# # crud/permission.py
# from typing import List, Optional
# from sqlalchemy.orm import Session
# from app.models.authsystem.Permission import Permission
# from app.schemas.authsystem.permission import PermissionCreate, PermissionUpdate

# class CRUDPermission:
#     def get(self, db: Session, id: str) -> Optional[Permission]:
#         return db.query(Permission).filter(Permission.id == id).first()

#     def get_by_name(self, db: Session, name: str) -> Optional[Permission]:
#         return db.query(Permission).filter(Permission.name == name).first()

#     def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Permission]:
#         return db.query(Permission).offset(skip).limit(limit).all()

#     def create(self, db: Session, *, obj_in: PermissionCreate, role_id: str) -> Permission:
#         db_obj = Permission(
#             name=obj_in.name,
#             description=obj_in.description,
#             resource=obj_in.resource,
#             action=obj_in.action,
#             role_id=role_id
#         )
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj

#     def update(self, db: Session, *, db_obj: Permission, obj_in: PermissionUpdate) -> Permission:
#         if isinstance(obj_in, dict):
#             update_data = obj_in
#         else:
#             update_data = obj_in.model_dump(exclude_unset=True)
        
#         for field, value in update_data.items():
#             setattr(db_obj, field, value)
            
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj

#     def delete(self, db: Session, *, id: str) -> Permission:
#         obj = db.query(Permission).get(id)
#         db.delete(obj)
#         db.commit()
#         return obj

#     def get_role_permissions(self, db: Session, role_id: str) -> List[Permission]:
#         return db.query(Permission).filter(Permission.role_id == role_id).all()

# permission = CRUDPermission()

from app.models.authsystem.permission import Permission
from app.crud.base import CRUDBase

crud_permission = CRUDBase(Permission)
# # crud/role.py
# from typing import List, Optional
# from sqlalchemy.orm import Session
# from app.models.authsystem.role import Role
# from app.schemas.authsystem.role import RoleCreate, RoleUpdate

# class CRUDRole:
#     def get(self, db: Session, id: str) -> Optional[Role]:
#         return db.query(Role).filter(Role.id == id).first()

#     def get_by_name(self, db: Session, name: str) -> Optional[Role]:
#         return db.query(Role).filter(Role.name == name).first()

#     def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Role]:
#         return db.query(Role).offset(skip).limit(limit).all()

#     def create(self, db: Session, *, obj_in: RoleCreate, user_id: str) -> Role:
#         db_obj = Role(
#             name=obj_in.name,
#             description=obj_in.description,
#             user_id=user_id
#         )
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj

#     def update(self, db: Session, *, db_obj: Role, obj_in: RoleUpdate) -> Role:
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

#     def delete(self, db: Session, *, id: str) -> Role:
#         obj = db.query(Role).get(id)
#         db.delete(obj)
#         db.commit()
#         return obj

#     def get_user_roles(self, db: Session, user_id: str) -> List[Role]:
#         return db.query(Role).filter(Role.user_id == user_id).all()

# role = CRUDRole()

from app.models.authsystem.role import Role
from app.crud.base import CRUDBase

crud_role = CRUDBase(Role)
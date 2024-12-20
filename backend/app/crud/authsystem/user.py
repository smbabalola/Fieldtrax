# File: backend/app/crud/authsystem/user.py
from typing import Optional, List, Union, Dict, Any
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.authsystem.user import User
from app.schemas.authsystem.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        """Create new user with hashed password"""
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_active=obj_in.is_active if hasattr(obj_in, 'is_active') else True,
            is_verified=obj_in.is_verified if hasattr(obj_in, 'is_verified') else False
        )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise e

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """Update user"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        if update_data.get("password"):
            update_data["password"] = get_password_hash(update_data["password"])
        
        try:
            return super().update(db, db_obj=db_obj, obj_in=update_data)
        except Exception as e:
            db.rollback()
            raise e

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """Check if user is active"""
        return user.is_active

    def is_verified(self, user: User) -> bool:
        """Check if user is verified"""
        return user.is_verified

crud_user = CRUDUser(User)

# from app.models.authsystem.user import User
# from app.crud.base import CRUDBase

# crud_user = CRUDBase(User)
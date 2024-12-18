# # File: backend/app/crud/authsystem/password_reset.py
# from typing import Optional
# from datetime import datetime, timedelta
# from sqlalchemy.orm import Session
# from app.crud.base import CRUDBase
# from app.models.authsystem.password_reset import PasswordReset
# from app.schemas.authsystem.password_reset import PasswordResetCreate, PasswordResetUpdate
# from app.core.security import generate_reset_token

# class CRUDPasswordReset(CRUDBase[PasswordReset, PasswordResetCreate, PasswordResetUpdate]):
#     async def create_reset_token(self, db: Session, *, user_id: str) -> PasswordReset:
#         """Create new password reset token"""
#         # Delete any existing unused tokens
#         db.query(PasswordReset).filter(
#             PasswordReset.user_id == user_id,
#             PasswordReset.is_used == False
#         ).delete()
        
#         # Create new token
#         token = generate_reset_token(user_id)
#         db_obj = PasswordReset(
#             user_id=user_id,
#             token=token,
#             expires_at=datetime.utcnow() + timedelta(hours=24),
#             is_used=False
#         )
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj

#     async def get_valid_token(self, db: Session, *, token: str) -> Optional[PasswordReset]:
#         """Get valid (unused and not expired) token"""
#         return db.query(PasswordReset).filter(
#             PasswordReset.token == token,
#             PasswordReset.is_used == False,
#             PasswordReset.expires_at > datetime.utcnow()
#         ).first()

#     async def mark_used(self, db: Session, *, db_obj: PasswordReset) -> PasswordReset:
#         """Mark token as used"""
#         db_obj.is_used = True
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj

# crud_password_reset = CRUDPasswordReset(PasswordReset)

from app.models.authsystem.password_reset import PasswordReset
from app.crud.base import CRUDBase

crud_password_reset = CRUDBase(PasswordReset)
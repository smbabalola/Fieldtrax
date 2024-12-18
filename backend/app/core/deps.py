# File: backend/app/core/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.crud.authsystem.user_session import crud_user_session
from app.crud.authsystem.user import crud_user
from app.schemas.authsystem.user_session import UserSessionResponse
from app.schemas.authsystem.user import UserResponse
from app.db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_session(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserSessionResponse:
    """Get current active session from access token"""
    session = await crud_user_session.get_by_token(db=db, token=token)
    if not session or not session.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return session

async def get_current_user(
    current_session: UserSessionResponse = Depends(get_current_session),
    db: Session = Depends(get_db)
) -> UserResponse:
    """Get current authenticated user"""
    user = await crud_user.get(db=db, id=current_session.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )
    return user

async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    """Get current active user with additional verification checks"""
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified"
        )
    return current_user

async def get_current_admin_user(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    """Get current admin user"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
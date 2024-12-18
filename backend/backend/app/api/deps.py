# File: backend/app/api/deps.py
from typing import Generator, AsyncGenerator, Awaitable
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.models.authsystem.user import User
from app.core.config import settings
from app.db.session import SessionLocal
from app.core.security import security_utils, oauth2_scheme
from app.core.ws.manager import ConnectionManager, job_update_manager
from app.crud.authsystem.user import crud_user
from inspect import isawaitable

async def get_db() -> AsyncGenerator[Session, None]:
    """Dependency for getting database session"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Dependency for getting current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await crud_user.get(db, id=user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Awaitable[User] | User = Depends(get_current_user),
) -> User:
    """Dependency for getting current active user"""
    # Handle both coroutine and direct User objects
    user = await current_user if isawaitable(current_user) else current_user
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

async def get_job_update_manager() -> ConnectionManager:
    """Dependency for WebSocket connection manager"""
    return job_update_manager
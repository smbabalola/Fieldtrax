# File: backend/app/api/v1/endpoints/auth/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from app.crud.authsystem.user import crud_user
from app.crud.authsystem.user_session import crud_user_session
from app.schemas.authsystem.user_session import UserSessionBase as UserSession, UserSessionCreate
from app.core.deps import get_db, get_current_session
from app.core.security import create_access_token, create_refresh_token

router = APIRouter()

@router.post("/verify", response_model=dict)
async def verify_auth(
    current_session: UserSession = Depends(get_current_session),    
):
    """Verify authentication status"""
    return {"authenticated": True, "session_id": current_session.id}

@router.post("/logout")
async def logout(
    current_session: UserSession = Depends(get_current_session),
    db: Session = Depends(get_db)
):
    """Logout user"""
    await crud_user_session.deactivate_session(db=db, session_id=current_session.id)
    return {"message": "Successfully logged out"}

@router.post("/refresh", response_model=UserSession)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    session = await crud_user_session.get_by_refresh_token(db=db, refresh_token=refresh_token)
    if not session or not session.is_active:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    
    # Generate new tokens
    new_access_token = create_access_token()
    new_refresh_token = create_refresh_token()
    
    # Update session
    updated_session = await crud_user_session.update_tokens(
        db=db,
        session_id=session.id,
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )
    return updated_session
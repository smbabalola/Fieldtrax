# File: backend/app/api/v1/endpoints/auth/user.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.deps import get_db, get_current_user
from app.core.security import (
    verify_password,
    get_password_hash,
    generate_verification_token,
    verify_verification_token,
    generate_reset_token
)
from app.crud.authsystem.user import crud_user
from app.crud.authsystem.password_reset import crud_password_reset
from app.schemas.authsystem.user import UserResponse, UserCreate, UserUpdate
from app.schemas.authsystem.password_reset import PasswordResetCreate
from app.core.email import (
    send_verification_email,
    send_password_reset_email
)

router = APIRouter(
    # prefix="/auth",
    tags = ['users']
)

@router.post("/", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create new user"""
    # Check if user exists
    # user = await crud_user.get_by_email(db, email=user_in.email)
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    # user = await crud_user.create(db=db, obj_in=user_in)
    user = await run_in_threadpool(crud_user.create, db, user_in)
    
    # Generate verification token
    verification_token = generate_verification_token(user_id=user.id)
    
    # Update user with verification token
    user_update = UserUpdate(verification_token=verification_token)
    user = await crud_user.update(db=db, db_obj=user, obj_in=user_update)
    
    # Send verification email
    background_tasks.add_task(
        send_verification_email,
        email=user.email,
        verification_token=verification_token
    )
    
    return user

@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get current user"""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_in: UserUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user"""
    return await crud_user.update(db=db, db_obj=current_user, obj_in=user_in)

@router.post("/verify-email")
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """Verify user's email address using verification token"""
    user_id = verify_verification_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    user = await crud_user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_update = UserUpdate(
        is_verified=True,
        verification_token=None
    )
    await crud_user.update(db=db, db_obj=user, obj_in=user_update)
    
    return {"message": "Email successfully verified"}

@router.post("/send-verification")
async def send_verification(
    background_tasks: BackgroundTasks,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a new verification email to current user"""
    if current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    verification_token = generate_verification_token(current_user.id)
    user_update = UserUpdate(verification_token=verification_token)
    await crud_user.update(db=db, db_obj=current_user, obj_in=user_update)
    
    background_tasks.add_task(
        send_verification_email,
        email=current_user.email,
        token=verification_token
    )
    
    return {"message": "Verification email sent"}

@router.post("/forgot-password")
async def forgot_password(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Initiate password reset process"""
    # user = await crud_user.get_by_email(db=db, email=email)
    user = await run_in_threadpool(crud_user.get_by_email, db, email=email)
    if not user:
        # Don't reveal if email exists
        return {"message": "If email exists, password reset instructions will be sent"}
    
    reset_token = await crud_password_reset.create_reset_token(
        db=db,
        user_id=user.id
    )
    
    background_tasks.add_task(
        send_password_reset_email,
        email=user.email,
        token=reset_token.token
    )
    
    return {"message": "If email exists, password reset instructions will be sent"}

@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """Reset password using reset token"""
    reset_token = await crud_password_reset.get_valid_token(
        db=db,
        token=token
    )
    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    user = await crud_user.get(db=db, id=reset_token.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_update = UserUpdate(
        hashed_password=get_password_hash(new_password)
    )
    await crud_user.update(db=db, db_obj=user, obj_in=user_update)
    await crud_password_reset.mark_used(db=db, db_obj=reset_token)
    
    return {"message": "Password successfully reset"}

@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change password for authenticated user"""
    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    user_update = UserUpdate(
        hashed_password=get_password_hash(new_password)
    )
    await crud_user.update(db=db, db_obj=current_user, obj_in=user_update)
    
    return {"message": "Password successfully changed"}
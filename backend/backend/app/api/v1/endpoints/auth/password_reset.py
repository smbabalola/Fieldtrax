# File: backend/app/api/v1/endpoints/auth/password_reset.pyfrom fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from app.crud.authsystem.password_reset import crud_password_reset
from app.crud.authsystem.user import crud_user
from app.schemas.authsystem.password_reset import (
    PasswordResetCreate,
    PasswordResetResponse as PasswordReset
)
from app.core.deps import get_db
from app.core.security import get_password_hash, validate_password_strength
from app.core.email import send_password_reset_email
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/request-reset")
async def request_password_reset(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Request password reset token"""
    logger.info(f"Password reset requested for email: {email}")
    
    try:
        # Get user without revealing if email exists
        user = await run_in_threadpool(crud_user.get_by_email, db, email=email)
        if not user:
            logger.info(f"No user found for email: {email}")
            return {"message": "If email exists, password reset instructions will be sent"}

        # Create reset token
        reset_token = await crud_password_reset.create_reset_token(db=db, user_id=user.id)
        logger.info(f"Reset token created for user: {user.id}")

        # Send email in background
        background_tasks.add_task(
            send_password_reset_email,
            email=email,
            reset_token=reset_token.token
        )
        logger.info(f"Reset email queued for sending to: {email}")

        return {"message": "If email exists, password reset instructions will be sent"}
    
    except Exception as e:
        logger.error(f"Error in password reset request: {str(e)}")
        # Don't reveal internal errors to user
        return {"message": "If email exists, password reset instructions will be sent"}

@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """Reset password using token"""
    try:
        # Validate password strength
        password_validation = validate_password_strength(new_password)
        if not password_validation['meets_requirements']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Password does not meet requirements",
                    "requirements": password_validation['requirements'],
                    "feedback": password_validation['feedback']
                }
            )

        # Verify token
        reset_token = await crud_password_reset.get_valid_token(db=db, token=token)
        if not reset_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        # Get user
        user = await crud_user.get(db=db, id=reset_token.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update password
        hashed_password = get_password_hash(new_password)
        await crud_user.update(db=db, db_obj=user, obj_in={"password": hashed_password})

        # Mark token as used
        await crud_password_reset.mark_used(db=db, db_obj=reset_token)

        logger.info(f"Password reset successful for user: {user.id}")
        return {"message": "Password reset successful"}

    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in password reset: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while resetting password"
        )
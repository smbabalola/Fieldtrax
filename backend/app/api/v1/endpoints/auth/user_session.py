
# File: backend/app/api/v1/endpoints/auth/user_session.py
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.authsystem.user_session import crud_user_session
from app.schemas.authsystem.user_session import (
    UserSessionResponse,
    UserSessionCreate,
    UserSessionUpdate
)
from app.core.deps import get_db, get_current_user, get_current_session
from app.schemas.authsystem.user import UserResponse as User
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token
)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/token",  # Match the actual endpoint path
    auto_error=True
)

router = APIRouter()

# Add login request model
class LoginRequest(BaseModel):
    email: str
    password: str
    device_info: str | None = None
    ip_address: str | None = None

# @router.post("/token", response_model=UserSessionResponse)
# async def login_for_access_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     """OAuth2 compatible token login"""
#     user = await crud_user_session.authenticate(
#         db=db,
#         email=form_data.username,
#         password=form_data.password
#     )
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token = create_access_token(data={"sub": user.id})
#     refresh_token = create_refresh_token(data={"sub": user.id})

#     session = await crud_user_session.create_session(
#         db=db,
#         user_id=user.id,
#         access_token=access_token,
#         refresh_token=refresh_token
#     )

#     return session


@router.post("/login", response_model=UserSessionResponse)
async def login_json(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login endpoint for JSON requests"""
    user = await crud_user_session.authenticate(
        db=db,
        email=login_data.email,
        password=login_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # Create tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    # Create session
    session = await crud_user_session.create_session(
        db=db,
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
        device_info=login_data.device_info,
        ip_address=login_data.ip_address
    )

    return session

# Form data login endpoint
@router.post("/login/form", response_model=UserSessionResponse)
async def login_form(
    email: str = Form(...),
    password: str = Form(...),
    device_info: Optional[str] = Form(None),
    ip_address: Optional[str] = Form(None),

    db: Session = Depends(get_db)
):
    """Login endpoint for form data"""
    user = await crud_user_session.authenticate(db=db, email=email, password=password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # Create tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    # Create session
    session = await crud_user_session.create_session(
        db=db,
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
        device_info=device_info,
        ip_address=ip_address
    )

    return session

# @router.post("/token", response_model=UserSessionResponse)
# async def login_for_access_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     """OAuth2 compatible token login"""
#     user = await crud_user_session.authenticate(
#         db=db,
#         email=form_data.username,
#         password=form_data.password
#     )
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token = create_access_token(data={"sub": user.id})
#     refresh_token = create_refresh_token(data={"sub": user.id})

#     session = await crud_user_session.create_session(
#         db=db,
#         user_id=user.id,
#         access_token=access_token,
#         refresh_token=refresh_token
#     )

#     return session

@router.post("/token", response_model=UserSessionResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 compatible token login"""
    try:
        print(f"Token endpoint hit with username: {form_data.username}")  # Debug print
        user = await crud_user_session.authenticate(
            db=db,
            email=form_data.username,
            password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )

        access_token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})

        session = await crud_user_session.create_session(
            db=db,
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token
        )

        return session
    except Exception as e:
        print(f"Error in token endpoint: {str(e)}")  # Debug print
        raise

@router.post("/refresh", response_model=UserSessionResponse)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Refresh access token"""
    print("Refresh token endpoint hit")  # Debugging statement
    try:
        payload = verify_token(refresh_token, token_type="refresh")
        user_id = payload.get("sub")
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Create new tokens
    access_token = create_access_token(data={"sub": user_id})
    new_refresh_token = create_refresh_token(data={"sub": user_id})

    # Update session
    session = await crud_user_session.get_by_refresh_token(db=db, refresh_token=refresh_token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    updated_session = await crud_user_session.update(
        db=db,
        db_obj=session,
        obj_in={
            "access_token": access_token,
            "refresh_token": new_refresh_token
        }
    )

    return updated_session

@router.get("/active", response_model=List[UserSessionResponse])
async def get_active_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all active sessions for current user"""
    return await crud_user_session.get_active_sessions(db=db, user_id=current_user.id)

@router.post("/logout")
async def logout(
    current_session: UserSessionResponse = Depends(get_current_session),
    db: Session = Depends(get_db)
):
    """Logout current session"""
    await crud_user_session.deactivate_session(db=db, session_id=current_session.id)
    return {"message": "Successfully logged out"}

@router.post("/logout/all")
async def logout_all(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout all sessions for current user"""
    await crud_user_session.deactivate_all_sessions(db=db, user_id=current_user.id)
    return {"message": "Successfully logged out all sessions"}

@router.put("/update-activity")
async def update_last_activity(
    current_session: UserSessionResponse = Depends(get_current_session),
    db: Session = Depends(get_db)
):
    """Update last activity timestamp"""
    await crud_user_session.update_last_activity(db=db, session_id=current_session.id)
    return {"message": "Activity timestamp updated"}
# app/core/auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import User
# from app.core.auth import verify_password


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Here you would typically query your database to get the user
    # For now, we'll return the email as the user identifier
    return {"email": email}

# async def authenticate_user(db, email: EmailStr, password: str):
#     # This is a placeholder - you'll need to implement actual database queries
#     user = None  # await get_user_by_email(email)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
# from pydantic import EmailStr

async def authenticate_user(db: Session, username: str, password: str):
    try:
        # Query the database for the user by email
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            return False
        
        # Verify the password
        if not verify_password(password, user.hashed_password):
            return False
        
        return user
    
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed due to an internal error."
        )

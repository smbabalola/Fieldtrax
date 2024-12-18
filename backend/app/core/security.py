# File: backend/app/core/security.py
# File: backend/app/core/security.py
from datetime import datetime, timedelta
import hashlib
import os
from typing import Optional, Dict
from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from app.core.email import EmailService
from pydantic import EmailStr
import secrets
import string
# import jwt
from zxcvbn import zxcvbn  # For enhanced password strength checking
from fastapi.security import OAuth2PasswordBearer

# Create OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

class SecurityUtils:
    def __init__(self):
        self.pwd_chars = string.ascii_letters + string.digits + string.punctuation
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def generate_token(self, length: int = 32) -> str:
        """Generate a secure random token"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def validate_password_strength(self, password: str) -> Dict:
        """
        Enhanced password strength validation
        Returns a dictionary with validation details and zxcvbn score
        """
        # Basic requirements check
        basic_requirements = {
            "length": len(password) >= 8,
            "uppercase": any(c.isupper() for c in password),
            "lowercase": any(c.islower() for c in password),
            "digit": any(c.isdigit() for c in password),
            "special": any(c in string.punctuation for c in password)
        }

        # Advanced strength check using zxcvbn
        strength_check = zxcvbn(password)
        
        return {
            "meets_requirements": all(basic_requirements.values()),
            "requirements": basic_requirements,
            "strength_score": strength_check['score'],  # 0-4
            "feedback": strength_check['feedback'],
            "estimated_crack_time": strength_check['crack_times_display']['offline_slow_hashing_1e4_per_second']
        }

    def validate_token_expiry(self, created_at: datetime, expire_hours: int = 24) -> bool:
        """Check if a token has expired"""
        expiry_time = created_at + timedelta(hours=expire_hours)
        return datetime.utcnow() <= expiry_time

    def get_password_hash(self, password: str) -> str:
        """Hash password using bcrypt"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password using bcrypt"""
        return self.pwd_context.verify(plain_password, hashed_password)

class TokenService:
    def __init__(self):
        self.security_utils = SecurityUtils()
        self.email_service = EmailService()
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
        self.reset_token_expire_hours = settings.RESET_TOKEN_EXPIRE_HOURS
        self.verification_token_expire_hours = 48  # 48 hours for email verification

    def create_access_token(self, data: dict) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, data: dict) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def generate_reset_token(self, user_id: str) -> str:
        """Generate password reset token"""
        to_encode = {"user_id": user_id, "type": "reset"}
        expire = datetime.utcnow() + timedelta(hours=self.reset_token_expire_hours)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_reset_token(self, user_id: str) -> str:
        """Create password reset token"""
        to_encode = {"user_id": user_id, "type": "reset"}
        expire = datetime.utcnow() + timedelta(hours=self.reset_token_expire_hours)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str, token_type: str = "access") -> dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != token_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Invalid token type. Expected {token_type}"
                )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

    def verify_reset_token(self, token: str) -> Optional[str]:
        """Verify password reset token and return user_id if valid"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != "reset":
                return None
            return payload.get("user_id")
        except JWTError:
            return None

    def verify_verification_token(self, token: str) -> Optional[str]:
        """Verify email verification token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != "verification":
                return None
            return payload.get("user_id")
        except JWTError:
            return None
    
    def generate_verification_token(self, user_id: str) -> str:
        """Generate email verification token"""
        to_encode = {"user_id": user_id, "type": "verification"}
        expire = datetime.utcnow() + timedelta(hours=self.verification_token_expire_hours)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def send_password_reset_email(self, email: EmailStr, reset_token: str) -> bool:
        """Send password reset email"""
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        return await self.email_service.send_reset_email(email, reset_link)

    async def send_verification_email(self, email: EmailStr, verification_token: str) -> bool:
        """Send email verification email"""
        verification_link = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
        return await self.email_service.send_verification_email(email, verification_link)

class SessionManager:
    def __init__(self):
        self.security_utils = SecurityUtils()

    def create_session_id(self) -> str:
        """Generate a unique session ID"""
        return self.security_utils.generate_token(48)

    def generate_device_id(self, user_agent: str, ip_address: str) -> str:
        """Generate a unique device identifier"""
        device_string = f"{user_agent}:{ip_address}"
        return hashlib.sha256(device_string.encode()).hexdigest()

# Create instances for export
security_utils = SecurityUtils()
token_service = TokenService()
session_manager = SessionManager()

# Export commonly used functions
get_password_hash = security_utils.get_password_hash
verify_password = security_utils.verify_password
validate_password_strength = security_utils.validate_password_strength
validate_token_expiry = security_utils.validate_token_expiry

create_access_token = token_service.create_access_token
create_refresh_token = token_service.create_refresh_token
create_reset_token = token_service.create_reset_token
generate_reset_token = token_service.generate_reset_token
verify_token = token_service.verify_token
verify_reset_token = token_service.verify_reset_token
verify_verification_token = token_service.verify_verification_token
send_password_reset_email = token_service.send_password_reset_email
send_verification_email = token_service.send_verification_email

generate_verification_token = token_service.generate_verification_token

create_session_id = session_manager.create_session_id
generate_device_id = session_manager.generate_device_id
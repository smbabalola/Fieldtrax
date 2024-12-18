# File: backend/app/crud/authsystem/user_session.py
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.authsystem.user_session import UserSession
from app.models.authsystem.user import User
from app.schemas.authsystem.user_session import (
    UserSessionCreate,
    UserSessionUpdate,
    DeviceInfo
)
from app.core.security import generate_device_id, verify_password
from app.crud.base import CRUDBase
from user_agents import parse

class CRUDUserSession(CRUDBase[UserSession, UserSessionCreate, UserSessionUpdate]):
    async def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def create_session(
        self,
        db: Session,
        *,
        user_id: str,
        access_token: str,
        refresh_token: Optional[str] = None,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> UserSession:
        """Create new user session"""
        # Enhanced device info while maintaining compatibility
        enhanced_device_info = device_info
        if device_info and '|' not in device_info:  # Not already in enhanced format
            try:
                ua = parse(device_info)
                enhanced_device_info = DeviceInfo(
                    device_type=ua.device.family,
                    os=f"{ua.os.family} {ua.os.version_string}",
                    browser=f"{ua.browser.family} {ua.browser.version_string}",
                    is_mobile=ua.is_mobile,
                    is_tablet=ua.is_tablet,
                    is_pc=ua.is_pc
                ).to_str()
            except:
                pass  # Keep original device_info if parsing fails

        db_obj = UserSession(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=1),
            created_at=datetime.now(timezone.utc),
            is_active=True,
            device_info=enhanced_device_info,
            ip_address=ip_address
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def get_active_sessions(
        self,
        db: Session,
        *,
        user_id: str
    ) -> List[UserSession]:
        """Get all active sessions for user"""
        return db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.now(timezone.utc)
        ).all()

    async def update_last_activity(
        self,
        db: Session,
        *,
        session_id: str
    ) -> Optional[UserSession]:
        """Update last activity timestamp"""
        session = await self.get(db=db, id=session_id)
        if session:
            session.last_activity = datetime.now(timezone.utc)
            db.add(session)
            db.commit()
            db.refresh(session)
        return session

    async def deactivate_session(
        self,
        db: Session,
        *,
        session_id: str
    ) -> Optional[UserSession]:
        """Deactivate a session"""
        session = await self.get(db=db, id=session_id)
        if session:
            session.is_active = False
            session.last_activity = datetime.now(timezone.utc)
            db.add(session)
            db.commit()
            db.refresh(session)
        return session

    async def deactivate_all_sessions(
        self,
        db: Session,
        *,
        user_id: str
    ) -> None:
        """Deactivate all sessions for a user"""
        sessions = await self.get_active_sessions(db=db, user_id=user_id)
        for session in sessions:
            session.is_active = False
            session.last_activity = datetime.now(timezone.utc)
        db.commit()

    async def get_by_token(
        self,
        db: Session,
        *,
        token: str
    ) -> Optional[UserSession]:
        """Get session by access token"""
        return db.query(UserSession).filter(
            UserSession.access_token == token,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.now(timezone.utc)
        ).first()

    async def get_by_refresh_token(
        self,
        db: Session,
        refresh_token: str
    ) -> Optional[UserSession]:
        """Get session by refresh token"""
        return db.query(UserSession).filter(
            UserSession.refresh_token == refresh_token,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.now(timezone.utc)
        ).first()

    def is_session_valid(self, session: UserSession) -> bool:
        """Check if session is valid"""
        return (
            session.is_active and
            session.expires_at > datetime.now(timezone.utc)
        )

crud_user_session = CRUDUserSession(UserSession)

# from app.models.authsystem.user_session import UserSession
# from app.crud.base import CRUDBase

# crud_user_session = CRUDBase(UserSession)
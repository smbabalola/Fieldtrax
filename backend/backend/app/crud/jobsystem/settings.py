# /backend/app/crud/jobsystem/settings.py
from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.settings import UserSetting
from app.schemas.jobsystem.settings import UserSettingCreate, UserSettingUpdate

class CRUDUserSetting(CRUDBase[UserSetting, UserSettingCreate, UserSettingUpdate]):
    async def get_by_user(
        self, 
        db: Session, 
        *, 
        user_id: int
    ) -> Optional[UserSetting]:
        return db.query(UserSetting).filter(
            UserSetting.user_id == user_id
        ).first()

    async def create_or_update(
        self,
        db: Session,
        *,
        user_id: int,
        obj_in: UserSettingCreate
    ) -> UserSetting:
        db_obj = await self.get_by_user(db, user_id=user_id)
        if db_obj:
            return await self.update(db, db_obj=db_obj, obj_in=obj_in)
        return await self.create(db, obj_in=obj_in)

crud_user_setting = CRUDUserSetting(UserSetting)
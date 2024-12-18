from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, Dict
import logging

from app.api import deps
from app.models.authsystem.user import User
from app.schemas.jobsystem.settings import UserSetting, UserSettingCreate, UserSettingUpdate
from app.crud.jobsystem.settings import crud_user_setting
from app.core.constants import REGION_PRESETS

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
async def get_settings(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
) -> Any:
    """Get user settings"""
    try:
        logger.info(f"Fetching settings for user {current_user.id}")
        settings = await crud_user_setting.get_by_user(
            db, user_id=current_user.id
        )
        
        if not settings:
            logger.info(f"No settings found for user {current_user.id}, creating default")
            default_settings = UserSettingCreate(
                unit_system="US",
                unit_preferences=REGION_PRESETS["US"],
                display_settings={
                    "decimalPlaces": {
                        "length": 2,
                        "pressure": 1,
                        "temperature": 1,
                        "weight": 1,
                        "volume": 1,
                        "density": 2,
                        "torque": 0
                    },
                    "fontSize": "medium",
                    "darkMode": False,
                    "highContrast": False
                }
            )
            settings = await crud_user_setting.create(
                db, obj_in=default_settings
            )
        
        # Return in the format expected by the frontend
        return {
            "unit_system": settings.unit_system,
            "unit_preferences": settings.unit_preferences,
            "display_settings": settings.display_settings
        }
        
    except Exception as e:
        logger.error(f"Error fetching settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.put("/", response_model=Dict[str, Any])
async def update_settings(
    *,
    settings_in: UserSettingUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
) -> Any:
    """Update user settings"""
    try:
        settings = await crud_user_setting.get_by_user(db, user_id=current_user.id)
        if not settings:
            settings = await crud_user_setting.create(
                db, 
                obj_in=UserSettingCreate(
                    user_id=current_user.id,
                    **settings_in.dict()
                )
            )
        else:
            settings = await crud_user_setting.update(
                db,
                db_obj=settings,
                obj_in=settings_in
            )
            
        # Return in the format expected by the frontend
        return {
            "unit_system": settings.unit_system,
            "unit_preferences": settings.unit_preferences,
            "display_settings": settings.display_settings
        }
    except Exception as e:
        logger.error(f"Error updating settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/reset", response_model=Dict[str, Any])
async def reset_settings(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
) -> Any:
    """Reset user settings to defaults"""
    try:
        default_settings = UserSettingCreate(
            unit_system="US",
            unit_preferences=REGION_PRESETS["US"],
            display_settings={
                "decimalPlaces": {
                    "length": 2,
                    "pressure": 1,
                    "temperature": 1,
                    "weight": 1,
                    "volume": 1,
                    "density": 2,
                    "torque": 0
                },
                "fontSize": "medium",
                "darkMode": False,
                "highContrast": False
            }
        )
        
        settings = await crud_user_setting.get_by_user(db, user_id=current_user.id)
        if settings:
            settings = await crud_user_setting.update(
                db,
                db_obj=settings,
                obj_in=default_settings
            )
        else:
            settings = await crud_user_setting.create(
                db, 
                obj_in=default_settings
            )
            
        return {
            "unit_system": settings.unit_system,
            "unit_preferences": settings.unit_preferences,
            "display_settings": settings.display_settings
        }
    except Exception as e:
        logger.error(f"Error resetting settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
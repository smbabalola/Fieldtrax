# /backend/app/schemas/jobsystem/settings.py
from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel, Field

from app.models.base import TimeStampSchema

class UnitPreferences(BaseModel):
    lengthUnit: str = Field("ft", description="Length unit")
    pressureUnit: str = Field("psi", description="Pressure unit")
    temperatureUnit: str = Field("f", description="Temperature unit")
    weightUnit: str = Field("lbs", description="Weight unit")
    volumeUnit: str = Field("bbl", description="Volume unit")
    densityUnit: str = Field("ppg", description="Density unit")
    torqueUnit: str = Field("ft-lbs", description="Torque unit")
    rotationUnit: str = Field("rpm", description="Rotation unit")

class DecimalPlaces(BaseModel):
    length: int = 2
    pressure: int = 1
    temperature: int = 1
    weight: int = 1
    volume: int = 1
    density: int = 2
    torque: int = 0

class DisplaySettings(BaseModel):
    decimalPlaces: DecimalPlaces
    fontSize: str = "medium"
    darkMode: bool = False
    highContrast: bool = False

class UserSettingBase(TimeStampSchema):
    user_id: str
    unit_system: str
    unit_preferences: UnitPreferences
    display_settings: DisplaySettings

class UserSettingCreate(UserSettingBase):
    user_id: str
    unit_system: str
    unit_preferences: UnitPreferences
    display_settings: DisplaySettings
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class UserSettingUpdate(UserSettingBase):
    pass

class UserSetting(UserSettingBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True
# /backend/app/models/jobsystem/settings.py
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class UserSetting(BaseDBModel):
    __tablename__ = "user_settings"
    
    # id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("users.id"))
    
    # Unit system: "US", "METRIC", or "CUSTOM"
    unit_system = Column(String, default="US") 
    
    # Stores unit preferences if using custom system
    unit_preferences = Column(JSON, default={
        "lengthUnit": "ft",
        "pressureUnit": "psi", 
        "temperatureUnit": "f",
        "weightUnit": "lbs",
        "volumeUnit": "bbl",
        "densityUnit": "ppg",
        "torqueUnit": "ft-lbs",
        "rotationUnit": "rpm"
    })
    
    # Stores number formatting and display preferences
    display_settings = Column(JSON, default={
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
    })

    user = relationship("User", back_populates="settings")
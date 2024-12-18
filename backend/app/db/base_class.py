# File: backend/app/db/base_class.py
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, DateTime, String
from datetime import datetime
import uuid

@as_declarative()
class Base:
    id: Any
    __name__: str
    

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    # Generate UUID for id field
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Generate __tablename__ automatically
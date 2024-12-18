# File: app/models/authsystem/permission.py
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseDBModel

class Permission(BaseDBModel):
    __tablename__ = 'permissions'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(200))
    resource = Column(String(50), nullable=False)
    action = Column(String(20), nullable=False)

    role_id = Column(String(50), ForeignKey('roles.id'), nullable=False)
    role = relationship('Role', back_populates='permissions')

    def __repr__(self):
        return f"<Permission: {self.name}>"

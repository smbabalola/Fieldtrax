# File: app/models/authsystem/role.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base import BaseDBModel
from app.models.authsystem.associations import user_roles_table
from app.models.authsystem.permission import Permission

class Role(BaseDBModel):
    __tablename__ = 'roles'

    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(200))

    permissions = relationship('Permission', back_populates='role')
    users = relationship('User', secondary=user_roles_table, back_populates='roles')

    def __repr__(self):
        return f"<Role: {self.name}>"
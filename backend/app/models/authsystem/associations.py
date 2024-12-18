# File: app/models/authsystem/associations.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

# app/models/authsystem/associations.py
from sqlalchemy import Table, Column, String, ForeignKey
from app.database import Base

user_roles_table = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', String(50), ForeignKey('users.id'), primary_key=True),
    Column('role_id', String(50), ForeignKey('roles.id'), primary_key=True)
)
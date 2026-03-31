from sqlalchemy import Table, Column, ForeignKey
from db.base import Base

UserRoles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', ForeignKey('app_users.id'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True)
)
from sqlalchemy import ForeignKey, Table, Column
from db.base import Base

RolePermissions = Table(
    'RolePermissions',
    Base.metadata,
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', ForeignKey('permissions.id'), primary_key=True),
)
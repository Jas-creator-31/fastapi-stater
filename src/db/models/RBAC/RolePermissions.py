from sqlalchemy import Table, Column, ForeignKey
from src.db.base import Base

RolePermissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.role_id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.permission_id"), primary_key=True),
)

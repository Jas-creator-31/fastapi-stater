from sqlalchemy import Table, Column, ForeignKey
from src.db.base import Base

UserRoles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("app_users.user_id"), primary_key=True),
    Column("role_id", ForeignKey("roles.role_id"), primary_key=True),
)

from pydantic import EmailStr
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.AppUsers import AppUser
from src.features.users.user import User

class UserRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    async def exist(self, email: EmailStr):   
        stmt = (
            select(AppUser)
            .where(
                and_(
                        AppUser.email == email,
                        AppUser.deleted_at == None  # noqa: E711
                    )
                )
            )
        result = await self.db.execute(stmt)
        user = result.scalars().one_or_none()
        if user is None:
            return None
        return User(
            user
        )
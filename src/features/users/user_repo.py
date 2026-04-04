from pydantic import EmailStr
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from src.db.models.AppUsers import AppUser
from src.features.users.user import User

class UserRepo:
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    async def exist(self, email: EmailStr):   
        stmt = (
            select(AppUser)
            .where(
                and_(
                        AppUser.email == email,
                        AppUser.deleted_at == None
                    )
                )
            )
        user = self.db.scalars(stmt).one()
        return User(
            user
        )
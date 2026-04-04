
from typing import Literal

from src.db.models.AppUsers import AppUser
from src.core.security.hashing_functions import verify_hash

class User:
    def __init__(self, user: AppUser) -> None:
        self.user = user

    async def varify_password(self, password: str) -> Literal[True]:
        return await verify_hash(password, self.user.password_hash)
    
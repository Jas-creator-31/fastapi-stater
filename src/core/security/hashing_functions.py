from typing import Literal

from argon2 import PasswordHasher

ph = PasswordHasher()


async def hash(plain: str) -> str:
    return ph.hash(plain)


async def verify_hash(plain: str, hashed: str) -> Literal[True]:
    return ph.verify(plain, hashed)

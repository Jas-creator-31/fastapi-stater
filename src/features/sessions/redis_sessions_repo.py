from src.features.sessions.types import RedisSessionValueType
from src.infra.redis.client import r

class RedisSessionsRepo:

    def __init__(self) -> None:
        pass

    async def set_token(self, session_id, value: RedisSessionValueType):
        r.setex(f"auth:session:{session_id}", 604800 , value )

    async def get_refresh_token(self, session_id):
        return r.get(f"auth:session:{session_id}")
    
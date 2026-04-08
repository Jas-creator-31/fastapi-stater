from redis.asyncio import Redis

from src.features.sessions.models import RedisSessionValueType

class RedisSessionsRepo:

    def __init__(self, redis) -> None:
        self.redis: Redis = redis

    async def set_token(self, session_id, value: RedisSessionValueType):
        await self.redis.hsetex(f"auth:session:{session_id}", 604800 , mapping=value.model_dump() ) # type: ignore

    async def get_refresh_token(self, session_id):
        return await self.redis.get(f"auth:session:{session_id}")
    
    async def update_refresh_hash(self, session_id, new_refresh_hash):
        pipe = self.redis.pipeline(transaction=True)
        pipe.hset(f"auth:session:{session_id}", "refresh_hesh", new_refresh_hash)
        pipe.expire(f"auth:session:{session_id}", 604800)
        await pipe.execute()


    
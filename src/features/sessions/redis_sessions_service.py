from datetime import datetime, timezone, timedelta

from redis.asyncio import Redis

from src.features.sessions.models import RedisSessionsSeviceReturn
from src.features.sessions.redis_sessions_repo import RedisSessionsRepo
from src.features.auth.services.token_service import TokenService
# from src.features.sessions.types import RedisSessionValueType
from src.core.context.request_context import request_metadata_context
from uuid import uuid4

class RedisSissionsService:
    def __init__(self, redis) -> None:
        self.redis: Redis = redis
        
    async def _create_redis_value(self, user_id, refresh_hash):
        request_metadata = request_metadata_context.get()
        now = datetime.now(timezone.utc)
        redis_value = {
            'user_id': user_id,
            'refresh_hash': refresh_hash,
            'absolute_expiry': now + timedelta(days=30),
            'ip_address': request_metadata.client_ip,
            'browser': request_metadata.user_agent.browser,
            'device_info': request_metadata.user_agent.device,
            'os': request_metadata.user_agent.os
        }
        return redis_value

    async def create_sission(self, user_id):
        token_service = TokenService()
        redis_sessions_repo = RedisSessionsRepo(self.redis)

        tokens = (
            await 
            token_service
            .issue_token_pair(user_id, "create", uuid4())
        )

        redis_value = (
            await 
            self._create_redis_value
            (
                user_id,
                tokens
                .hashed_refresh_token
            )
        )
        (
            await 
            redis_sessions_repo
            .set_token(
                tokens, 
                redis_value # type: ignore
            )
        )

        return tokens.access_token, tokens.refresh_token

    async def refresh_sission(self, user_id, sid):
        token_service = TokenService()
        repo = RedisSessionsRepo(self.redis)

        tokens = await token_service.issue_token_pair(user_id, "refresh", sid)
        await repo.update_refresh_hash(sid, tokens.hashed_refresh_token)
        return RedisSessionsSeviceReturn(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token
        )

        



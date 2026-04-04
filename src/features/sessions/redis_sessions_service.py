from src.features.sessions.redis_sessions_repo import RedisSessionsRepo
from src.features.auth.services.token_service import TokenService
from src.features.sessions.types import RedisSessionValueType
from src.core.context.request_context import request_metadata_context

class RedisSissionsService:
    def __init__(self) -> None:
        pass
        
    async def __create_redis_value(self, user_id, refresh_hash):
        request_metadata = request_metadata_context.get()
        redis_value: RedisSessionValueType = {
            'user_id': user_id,
            'refresh_hash': refresh_hash,
            'ip_address': request_metadata.client_ip,
            'browser': request_metadata.user_agent.browser,
            'device_info': request_metadata.user_agent.device,
            'os': request_metadata.user_agent.os
        }
        return redis_value

    async def create_sission(self, user_id):
        token_service = TokenService()
        redis_sessions_repo = RedisSessionsRepo()

        tokens_metadata = (
            await 
            token_service
            .issue_jwt(user_id)
        )

        redis_value = (
            await 
            self.__create_redis_value
            (
                user_id,
                tokens_metadata
                .hashed_refresh_token
            )
        )
        (
            await 
            redis_sessions_repo
            .set_token(
                tokens_metadata, 
                redis_value
            )
        )

        return tokens_metadata.access_token, tokens_metadata.refresh_token






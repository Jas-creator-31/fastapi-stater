from redis.asyncio import Redis

from src.features.auth.services.token_service import TokenService
from src.features.users.user_repo import UserRepo
from src.features.auth.models import LoginPayload
from src.core.errors.domain_errors import AuthenticationError
from src.features.sessions.redis_sessions_service import RedisSissionsService


class AuthService:
    def __init__(self, db, redis):
        self.db = db
        self.redis: Redis = redis

    async def login(self, payload: LoginPayload):
        repo = UserRepo(self.db)
        redis_sessions_service = RedisSissionsService(self.redis)
        user_domain = await repo.exist(payload.email)
        if not user_domain or (not await user_domain.varify_password(payload.password)):
            raise AuthenticationError

        (
        access_token,
        refresh_token
        ) = await redis_sessions_service.create_sission(
            user_domain.user.user_id
        )

        return access_token, refresh_token
    
    async def refresh(self, refresh_token):
        token_service = TokenService()
        session_service = RedisSissionsService(self.redis)
        decoded_refresh_token = await token_service.varify_token(refresh_token)
        sid = decoded_refresh_token.sid
        user_id = decoded_refresh_token.sub
        tokens = await session_service.refresh_sission(
            user_id, 
            sid
        )
        return tokens


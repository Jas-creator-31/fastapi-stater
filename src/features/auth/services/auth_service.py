from src.features.users.user_repo import UserRepo
from src.features.auth.models import LoginPayload
from src.core.errors.domainErrors import AuthenticationError
from src.features.sessions.redis_sessions_service import RedisSissionsService
class AuthService:
    def __init__(self, db):
        self.db = db

    async def login(self, payload: LoginPayload):
        repo = UserRepo(self.db)
        redis_sessions_service = RedisSissionsService()
        user_domain = await repo.exist(payload.email)
        if not user_domain or (
            not await user_domain
            .varify_password(payload.password)
        ):
            raise AuthenticationError
        
        (
            access_token, 
            refresh_token
        ) = (
            await 
            redis_sessions_service
            .create_sission(user_domain.user.user_id)
        )

        return access_token, refresh_token

        

from fastapi import APIRouter, Depends, Response, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.deps import get_async_db
from src.features.auth.services.auth_service import AuthService
from src.infra.redis.client import get_redis
from src.features.auth.models import LoginPayload
from src.core.rate_limiting.limiter import limiter


route = APIRouter()

@route.post('/login')
@limiter.limit('5/minute')
async def login(
	request: Request,
    res: Response,
    payload: LoginPayload,
    db: AsyncSession = Depends(get_async_db),
	redis: Redis = Depends(get_redis)
):

	service = AuthService(db, redis)

	(access_token, refresh_token) = await service.login(payload)

	res.set_cookie(
        key="access_token",
        value=access_token,
        max_age=900,
        path="/",
        secure=True,
        samesite="none",
        httponly=True,
    )
    
	res.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=604800,
        path="/",
        secure=True,
        samesite="none",
        httponly=True,
    )

	return {"status": "success"}


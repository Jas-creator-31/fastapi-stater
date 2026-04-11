from fastapi import APIRouter, Depends, Request, Response
from redis.asyncio import Redis
from src.features.auth.services.auth_service import AuthService
from src.db.deps import get_async_db
from src.infra.redis.client import get_redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.rate_limiting.limiter import limiter


route = APIRouter()

@route.post("/refresh")
@limiter.limit('30/hour')
async def refresh(
    request: Request,
    res: Response,
    db: AsyncSession = Depends(get_async_db),
    redis: Redis = Depends(get_redis)
):
    refresh_token = request.cookies.get("refresh_token")
    service = AuthService(db, redis)
    tokens = await service.refresh(refresh_token)
    res.set_cookie(
        key="access_token",
        value=tokens.access_token,
        max_age=900,
        path="/",
        secure=True,
        samesite="none",
        httponly=True,
    )
    
    res.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        max_age=604800,
        path="/",
        secure=True,
        samesite="none",
        httponly=True,
    )

    return {"status": "success"}

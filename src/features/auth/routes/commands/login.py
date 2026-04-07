from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.deps import get_async_db
from src.features.auth.services.auth_service import AuthService
from src.main import limiter
from src.features.auth.models import LoginPayload

route = APIRouter()

@route.post('/login')
@limiter.limit('5/minute')
async def login(
    res: Response,
    payload: LoginPayload,
    db: AsyncSession = Depends(get_async_db),
):

	service = AuthService(db)

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


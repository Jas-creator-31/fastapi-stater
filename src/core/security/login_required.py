from functools import wraps
from fastapi import Request
from fastapi.responses import RedirectResponse

from src.features.auth.services.token_service import TokenService


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request") or next(
            (a for a in args if isinstance(a, Request)), None
        )
        access_token = request.cookies.get("access_token")
        service = TokenService()
        decoded_token = await service.varify_token(access_token)
        if not decoded_token:
            return RedirectResponse(url="/auth/refresh")
        result = await func(*args, **kwargs)
        return result

    return wrapper

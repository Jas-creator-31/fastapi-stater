from functools import wraps
from fastapi import Request
from fastapi.responses import RedirectResponse

from src.features.auth.services.token_service import TokenService


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        req = Request
        access_token = req.cookies.getter("access_token")
        service = TokenService()
        decoded_token = await service.varify_token(access_token)
        if not decoded_token:
            return RedirectResponse(url="/auth/refresh")
        result = func(*args, **kwargs)
        return result

    return wrapper

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
        is_logged_in = await service.varify_access_token(access_token)
        if not is_logged_in:
            return RedirectResponse(url="/auth/refresh")
        result = func(*args, **kwargs)
        return result

    return wrapper

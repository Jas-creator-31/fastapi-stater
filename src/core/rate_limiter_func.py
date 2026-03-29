from slowapi.util import get_remote_address
from fastapi import Request

async def rate_limiter_func(request: Request):
    user_session = request.cookies.get("user_session")
    if not user_session:
        return get_remote_address(request)
    return user_session
from fastapi import FastAPI, HTTPException, status
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


from src.core.errors.domainErrors import AuthenticationError


def exception_handler(app: FastAPI) -> None:
    @app.exception_handler(AuthenticationError)
    async def authentication_error() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    app.add_exception_handler(
        RateLimitExceeded,
        _rate_limit_exceeded_handler,  # type: ignore
    )

from fastapi import FastAPI, HTTPException, Request, status
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


from src.core.errors.domain_errors import (
    AuthenticationError,
    ExpiredJwtSignatureError,
    InvalidJwtSignatureError,
    InvalidJwtTokenError
)


def exception_handler(app: FastAPI) -> None:
    @app.exception_handler(AuthenticationError)
    async def authentication_error(request: Request, exc: AuthenticationError) -> None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    @app.exception_handler(ExpiredJwtSignatureError)
    async def expired_jwt_signature_error(request: Request, exc: ExpiredJwtSignatureError) -> None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=
            """
            The accesstoken has expired.
            Please use your refresh token to obtain a new one
            """,
        )
    
    @app.exception_handler(InvalidJwtSignatureError)
    async def invalid_jwt_signature_error(request: Request, exc: InvalidJwtSignatureError) -> None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="""
                The access token provided is invalid or malformed"
            """,
        )
    
    @app.exception_handler(InvalidJwtTokenError)
    async def invalid_jwt_token_error(request: Request, exc: InvalidJwtTokenError) -> None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=
            """
            The access token provided is invalid or malformed
            """,
        )

    app.add_exception_handler(
        RateLimitExceeded,
        _rate_limit_exceeded_handler,  # type: ignore
    )

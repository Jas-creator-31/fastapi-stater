from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
# from core.rate_limiter_func import rate_limiter_func
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
# import pytest

limiter = Limiter(
    key_func=get_remote_address,
    strategy="moving_window",
    default_limits=['200/day']
)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

origins = [
  "https://ledgeless-solvolytic-jesenia.ngrok-free.dev",
  "https://localhost",
  "https://192.168.31.190",
  "https://tijuana-unsymbolical-miss.ngrok-free.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # List of allowed origins
    allow_credentials=True,         # Allow cookies/authorization headers (requires specific origins)
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # Allow all HTTP request headers
)

app.get("/")
limiter.limit('5/hour')
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
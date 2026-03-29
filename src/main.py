from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from core.errors.exc_handler import exception_handler
# from core.rate_limiter_func import rate_limiter_func
from slowapi.util import get_remote_address
# import pytest

limiter = Limiter(
    key_func=get_remote_address,
    strategy="moving_window",
    default_limits=['200/day']
)

app = FastAPI()

app.state.limiter = limiter
exception_handler(app)

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
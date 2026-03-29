from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pytest

app = FastAPI()

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
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
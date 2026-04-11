from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.errors.exc_handler import exception_handler
from src.core.middleware.register_middleware import register_middleware
from src.features.auth.routes.auth import auth_router
from src.core.rate_limiting.limiter import limiter

app = FastAPI()

app.state.limiter = limiter

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

register_middleware(app)
exception_handler(app)

app.include_router(auth_router)

@app.get("/")
@limiter.exempt # type: ignore
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
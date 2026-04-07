from fastapi import APIRouter
from src.features.auth.routes.commands.login import route as login_route

auth_router = APIRouter(prefix="/auth", tags=["/auth"])

auth_router.include_router(login_route)
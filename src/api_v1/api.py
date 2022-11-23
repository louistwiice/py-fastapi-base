from fastapi import APIRouter

from api_v1.endpoints.users import router as users_router
from api_v1.endpoints.auth import router as auth_router

api_v1_router = APIRouter()
api_v1_router.include_router(users_router, prefix="/users")
api_v1_router.include_router(auth_router, prefix="/auth")

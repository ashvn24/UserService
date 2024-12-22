from fastapi import APIRouter
from routes.auth.auth import router as auth_router
from routes.userprocessor.createuser import router as create_user_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(create_user_router)
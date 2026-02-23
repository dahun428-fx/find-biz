from fastapi import APIRouter

from app.api.chat_ops import router as chat_ops_router
from app.api.install_runs import router as install_runs_router
from app.api.providers import router as providers_router
from app.api.skills import router as skills_router

api_router = APIRouter()
api_router.include_router(skills_router)
api_router.include_router(providers_router)
api_router.include_router(install_runs_router)
api_router.include_router(chat_ops_router)

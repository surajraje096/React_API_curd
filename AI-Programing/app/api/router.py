from fastapi import APIRouter

from app.api.chat import router as chat_router
from app.api.approvals import router as approvals_router
from app.api.logs import router as logs_router
from app.api.evaluations import router as evaluations_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(chat_router)
api_router.include_router(approvals_router)
api_router.include_router(logs_router)
api_router.include_router(evaluations_router)

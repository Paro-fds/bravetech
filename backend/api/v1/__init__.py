"""API Version 1 — Routers et endpoints v1.
"""

from fastapi import APIRouter
from backend.api.v1.candidatures import router as candidatures_router
from backend.api.v1.cursus import router as cursus_router
from backend.api.v1.auth import router as auth_router
from backend.api.v1.admin import router as admin_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(cursus_router)
api_v1_router.include_router(candidatures_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(admin_router)

__all__ = ["api_v1_router"]

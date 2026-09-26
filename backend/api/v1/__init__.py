"""API Version 1 — Routers et endpoints v1.
"""

from fastapi import APIRouter
from backend.api.v1.cursus import router as cursus_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(cursus_router)

__all__ = ["api_v1_router"]

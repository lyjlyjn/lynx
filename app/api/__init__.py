"""API router initialization."""
from fastapi import APIRouter

from .stream import router as stream_router
from .files import router as files_router
from .auth import router as auth_router
from .system import router as system_router

# Create main API router
api_router = APIRouter(prefix="/api")

# Include sub-routers
api_router.include_router(stream_router)
api_router.include_router(files_router)
api_router.include_router(auth_router)
api_router.include_router(system_router)

__all__ = ["api_router"]

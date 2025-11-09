"""Health check and system API endpoints."""
import logging
from fastapi import APIRouter
from datetime import datetime

from app.core import settings
from app.models import HealthResponse
from app.services import cache_service

logger = logging.getLogger(__name__)
router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow()
    )


@router.get("/stats")
async def get_stats():
    """Get system statistics."""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "cache": cache_service.get_stats(),
        "settings": {
            "chunk_size": settings.chunk_size,
            "max_chunk_size": settings.max_chunk_size,
            "enable_range_requests": settings.enable_range_requests,
            "allowed_extensions": settings.allowed_extensions_list,
        }
    }

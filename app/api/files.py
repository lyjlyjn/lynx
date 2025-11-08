"""File browsing API endpoints."""
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status

from app.core import get_current_user
from app.services import file_service
from app.models import FileInfo, DirectoryInfo

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/files", tags=["files"])


@router.get("/info/{file_path:path}", response_model=FileInfo)
async def get_file_info(
    file_path: str,
    current_user: str = Depends(get_current_user)
):
    """Get information about a specific file."""
    try:
        return await file_service.get_file_info(file_path)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found: {file_path}"
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.get("/list", response_model=DirectoryInfo)
@router.get("/list/{dir_path:path}", response_model=DirectoryInfo)
async def list_directory(
    dir_path: str = "/",
    current_user: str = Depends(get_current_user)
):
    """List contents of a directory."""
    try:
        return await file_service.list_directory(dir_path)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Directory not found: {dir_path}"
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

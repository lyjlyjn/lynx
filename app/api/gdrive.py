"""Google Drive proxy API endpoints."""
import logging
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/gdrive", tags=["gdrive"])


# ============ Response Models ============

class GDriveProxyResponse(BaseModel):
    """Google Drive proxy response"""
    status: str
    message: str
    data: Optional[dict] = None
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "File accessed successfully",
                "data": {"file_id": "abc123", "name": "video.mp4", "size": 5000000},
                "timestamp": "2025-11-11T13:26:47"
            }
        }


class GDriveListResponse(BaseModel):
    """Directory listing response"""
    status: str
    message: str
    files: list = []
    folder_count: int
    file_count: int
    total_size: int
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Directory listed successfully",
                "files": [{"name": "video.mp4", "size": 5000000}],
                "folder_count": 2,
                "file_count": 1,
                "total_size": 5000000,
                "timestamp": "2025-11-11T13:26:47"
            }
        }


class GDriveStreamResponse(BaseModel):
    """Google Drive stream URL response"""
    status: str
    file_name: str
    file_size: int
    mime_type: str
    stream_url: str
    supports_range: bool
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "file_name": "video.mp4",
                "file_size": 5000000,
                "mime_type": "video/mp4",
                "stream_url": "http://localhost:8000/api/stream/videos/video.mp4",
                "supports_range": True,
                "timestamp": "2025-11-11T13:26:47"
            }
        }


# ============ Endpoints ============

@router.get(
    "/proxy",
    response_model=GDriveProxyResponse,
    summary="Google Drive Proxy",
    description="Access Google Drive files via proxy with info/list/access operations"
)
async def gdrive_proxy(
    file_path: Optional[str] = Query(None, description="File path relative to mount point"),
    action: str = Query("info", description="Action: info | list | access"),
):
    """
    Google Drive proxy endpoint.
    
    Operations:
    - **info**: Get file information (requires file_path)
    - **list**: List directory (requires file_path)  
    - **access**: Verify access (no file_path needed)
    """
    try:
        from app.services import file_service
        from app.core import settings

        if action == "info" and file_path:
            file_info = await file_service.get_file_info(file_path)
            return GDriveProxyResponse(
                status="success",
                message=f"File info retrieved: {file_info.name}",
                data={
                    "path": file_info.path,
                    "name": file_info.name,
                    "size": file_info.size,
                    "mime_type": file_info.mime_type,
                    "type": file_info.type,
                },
                timestamp=datetime.utcnow()
            )
        
        elif action == "list" and file_path:
            directory_info = await file_service.list_directory(file_path)
            return GDriveProxyResponse(
                status="success",
                message=f"Directory listed: {file_path}",
                data={
                    "path": file_path,
                    "files": [f.name for f in directory_info.files],
                    "subdirectories": directory_info.subdirectories,
                },
                timestamp=datetime.utcnow()
            )
        
        elif action == "access":
            return GDriveProxyResponse(
                status="success",
                message="Access verified",
                data={"accessible": True},
                timestamp=datetime.utcnow()
            )
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid action: {action}. Use 'info', 'list', or 'access'"
            )
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Error in gdrive_proxy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/list",
    response_model=GDriveListResponse,
    summary="List Directory",
    description="List contents of a Google Drive directory"
)
async def gdrive_list(
    path: str = Query("/", description="Directory path to list"),
):
    """List directory contents."""
    try:
        from app.services import file_service

        directory_info = await file_service.list_directory(path)
        total_size = sum(f.size for f in directory_info.files)
        
        return GDriveListResponse(
            status="success",
            message=f"Directory listed: {path}",
            files=[{"name": f.name, "size": f.size} for f in directory_info.files],
            folder_count=len(directory_info.subdirectories),
            file_count=len(directory_info.files),
            total_size=total_size,
            timestamp=datetime.utcnow()
        )
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Directory not found: {path}")
    except Exception as e:
        logger.error(f"Error listing {path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/stream-url",
    response_model=GDriveStreamResponse,
    summary="Get Stream URL",
    description="Get streaming URL for a media file"
)
async def get_stream_url(
    file_path: str = Query(..., description="File path to stream"),
):
    """Get stream URL for a file."""
    try:
        from app.services import file_service
        from app.core import settings

        file_info = await file_service.get_file_info(file_path)
        stream_url = f"http://localhost:8000/api/stream{file_path}"
        
        return GDriveStreamResponse(
            status="success",
            file_name=file_info.name,
            file_size=file_info.size,
            mime_type=file_info.mime_type,
            stream_url=stream_url,
            supports_range=settings.enable_range_requests,
            timestamp=datetime.utcnow()
        )
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Error getting stream URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))
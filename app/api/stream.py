"""Streaming API endpoints."""
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Request, Response, Depends, status
from fastapi.responses import StreamingResponse

from app.core import settings, get_current_user
from app.services import file_service, cache_service, media_service
from app.models import StreamInfo, MediaMetadata

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/stream", tags=["streaming"])


def parse_range_header(range_header: str, file_size: int) -> tuple[int, int]:
    """Parse HTTP Range header."""
    try:
        range_str = range_header.replace('bytes=', '')
        parts = range_str.split('-')
        
        start = int(parts[0]) if parts[0] else 0
        end = int(parts[1]) if len(parts) > 1 and parts[1] else file_size - 1
        
        # Validate range
        if start < 0 or start >= file_size:
            raise ValueError("Invalid start position")
        if end >= file_size:
            end = file_size - 1
        if start > end:
            raise ValueError("Invalid range")
        
        return start, end
    except (ValueError, IndexError) as e:
        raise HTTPException(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail=f"Invalid range header: {e}"
        )


@router.get("/{file_path:path}")
async def stream_file(
    file_path: str,
    request: Request,
    response: Response,
    current_user: str = Depends(get_current_user)
):
    """
    Stream a file with support for HTTP Range requests.
    
    This endpoint supports resumable downloads and is optimized for large files.
    """
    try:
        # Get file info
        file_info = await file_service.get_file_info(file_path)
        file_size = file_info.size
        
        # Check if file is allowed
        if not file_info.extension in settings.allowed_extensions_list:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="File type not allowed"
            )
        
        # Parse range header if present
        range_header = request.headers.get('Range')
        
        if range_header and settings.enable_range_requests:
            # Parse range
            start, end = parse_range_header(range_header, file_size)
            content_length = end - start + 1
            
            # Create streaming response with range
            headers = {
                'Content-Range': f'bytes {start}-{end}/{file_size}',
                'Accept-Ranges': 'bytes',
                'Content-Length': str(content_length),
                'Content-Type': file_info.mime_type,
                'Content-Disposition': f'inline; filename="{file_info.name}"',
            }
            
            return StreamingResponse(
                file_service.stream_file(file_path, start, end),
                status_code=status.HTTP_206_PARTIAL_CONTENT,
                headers=headers,
                media_type=file_info.mime_type
            )
        else:
            # Stream entire file
            headers = {
                'Accept-Ranges': 'bytes',
                'Content-Length': str(file_size),
                'Content-Type': file_info.mime_type,
                'Content-Disposition': f'inline; filename="{file_info.name}"',
            }
            
            return StreamingResponse(
                file_service.stream_file(file_path),
                headers=headers,
                media_type=file_info.mime_type
            )
            
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
    except Exception as e:
        logger.error(f"Error streaming file {file_path}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.head("/{file_path:path}")
async def head_file(
    file_path: str,
    response: Response,
    current_user: str = Depends(get_current_user)
):
    """
    Get file headers without content (for checking file existence and size).
    """
    try:
        file_info = await file_service.get_file_info(file_path)
        
        response.headers['Accept-Ranges'] = 'bytes'
        response.headers['Content-Length'] = str(file_info.size)
        response.headers['Content-Type'] = file_info.mime_type
        response.headers['Content-Disposition'] = f'inline; filename="{file_info.name}"'
        
        return Response(status_code=status.HTTP_200_OK)
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found: {file_path}"
        )


@router.get("/{file_path:path}/info", response_model=StreamInfo)
async def get_stream_info(
    file_path: str,
    current_user: str = Depends(get_current_user)
):
    """Get streaming information for a file."""
    try:
        file_info = await file_service.get_file_info(file_path)
        
        return StreamInfo(
            file_path=file_path,
            file_size=file_info.size,
            content_type=file_info.mime_type,
            supports_range=settings.enable_range_requests,
            chunk_size=settings.chunk_size
        )
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found: {file_path}"
        )


@router.get("/{file_path:path}/metadata", response_model=Optional[MediaMetadata])
async def get_media_metadata(
    file_path: str,
    current_user: str = Depends(get_current_user)
):
    """Get media metadata for video/audio files."""
    try:
        # Check cache first
        cache_key = f"metadata:{file_path}"
        cached_metadata = await cache_service.get(cache_key)
        
        if cached_metadata:
            return MediaMetadata(**cached_metadata)
        
        # Get file info
        file_info = await file_service.get_file_info(file_path)
        
        if not file_info.is_streamable:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is not a media file"
            )
        
        # Get full path for ffprobe
        safe_path = file_service._get_safe_path(file_path)
        metadata = await media_service.get_metadata(str(safe_path))
        
        # Cache metadata
        if metadata:
            await cache_service.set(cache_key, metadata.model_dump())
        
        return metadata
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found: {file_path}"
        )

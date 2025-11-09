"""File management service."""
import os
import mimetypes
import logging
from typing import Optional, List, AsyncGenerator
from pathlib import Path
from datetime import datetime
import aiofiles
import asyncio

from app.core.config import settings
from app.models import FileInfo, DirectoryInfo, FileType

logger = logging.getLogger(__name__)


class FileService:
    """Service for managing files in CloudDrive2 mount."""
    
    def __init__(self):
        self.mount_path = Path(settings.clouddrive_mount_path).resolve()
        self.allowed_extensions = settings.allowed_extensions_list
        
        # Initialize mimetypes
        mimetypes.init()
        
    def _is_allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed."""
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        return ext in self.allowed_extensions
    
    def _get_file_type(self, mime_type: str) -> FileType:
        """Determine file type from MIME type."""
        if mime_type.startswith('video/'):
            return FileType.VIDEO
        elif mime_type.startswith('audio/'):
            return FileType.AUDIO
        elif mime_type.startswith('application/') or mime_type.startswith('text/'):
            return FileType.DOCUMENT
        else:
            return FileType.OTHER
    
    def _is_streamable(self, file_type: FileType, mime_type: str) -> bool:
        """Check if file is streamable."""
        return file_type in [FileType.VIDEO, FileType.AUDIO]
    
    def _get_safe_path(self, relative_path: str) -> Path:
        """Get safe absolute path within mount directory."""
        # Remove leading slash and resolve path
        clean_path = relative_path.lstrip('/')
        full_path = (self.mount_path / clean_path).resolve()
        
        # Resolve mount path for comparison
        resolved_mount = self.mount_path.resolve()
        
        # Ensure path is within mount directory (prevent directory traversal)
        try:
            full_path.relative_to(resolved_mount)
        except ValueError:
            raise PermissionError(f"Access denied: path outside mount directory")
        
        return full_path
    
    async def get_file_info(self, file_path: str) -> FileInfo:
        """Get information about a file."""
        safe_path = self._get_safe_path(file_path)
        
        if not safe_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not safe_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        # Get file stats
        stat = safe_path.stat()
        mime_type, _ = mimetypes.guess_type(str(safe_path))
        mime_type = mime_type or 'application/octet-stream'
        
        file_type = self._get_file_type(mime_type)
        extension = safe_path.suffix.lstrip('.')
        
        return FileInfo(
            name=safe_path.name,
            path=file_path,
            size=stat.st_size,
            type=file_type,
            extension=extension,
            modified=datetime.fromtimestamp(stat.st_mtime),
            mime_type=mime_type,
            is_streamable=self._is_streamable(file_type, mime_type)
        )
    
    async def list_directory(self, dir_path: str = "/") -> DirectoryInfo:
        """List contents of a directory."""
        safe_path = self._get_safe_path(dir_path)
        
        if not safe_path.exists():
            raise FileNotFoundError(f"Directory not found: {dir_path}")
        
        if not safe_path.is_dir():
            raise ValueError(f"Path is not a directory: {dir_path}")
        
        files = []
        subdirectories = []
        total_size = 0
        
        # List directory contents
        try:
            for entry in safe_path.iterdir():
                try:
                    if entry.is_file() and self._is_allowed_file(entry.name):
                        stat = entry.stat()
                        mime_type, _ = mimetypes.guess_type(str(entry))
                        mime_type = mime_type or 'application/octet-stream'
                        file_type = self._get_file_type(mime_type)
                        
                        # Create relative path
                        rel_path = str(entry.relative_to(self.mount_path))
                        if not rel_path.startswith('/'):
                            rel_path = '/' + rel_path
                        
                        files.append(FileInfo(
                            name=entry.name,
                            path=rel_path,
                            size=stat.st_size,
                            type=file_type,
                            extension=entry.suffix.lstrip('.'),
                            modified=datetime.fromtimestamp(stat.st_mtime),
                            mime_type=mime_type,
                            is_streamable=self._is_streamable(file_type, mime_type)
                        ))
                        total_size += stat.st_size
                    elif entry.is_dir():
                        subdirectories.append(entry.name)
                except (PermissionError, OSError) as e:
                    logger.warning(f"Cannot access {entry}: {e}")
                    continue
        except PermissionError as e:
            logger.error(f"Cannot list directory {safe_path}: {e}")
            raise
        
        return DirectoryInfo(
            name=safe_path.name or '/',
            path=dir_path,
            files=files,
            subdirectories=subdirectories,
            total_files=len(files),
            total_size=total_size
        )
    
    async def get_file_size(self, file_path: str) -> int:
        """Get file size."""
        safe_path = self._get_safe_path(file_path)
        
        if not safe_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return safe_path.stat().st_size
    
    async def stream_file(
        self,
        file_path: str,
        start: int = 0,
        end: Optional[int] = None
    ) -> AsyncGenerator[bytes, None]:
        """Stream file content with optional range."""
        safe_path = self._get_safe_path(file_path)
        
        if not safe_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_size = safe_path.stat().st_size
        
        # Validate range
        if start < 0 or start >= file_size:
            raise ValueError(f"Invalid start position: {start}")
        
        if end is None:
            end = file_size - 1
        elif end >= file_size:
            end = file_size - 1
        
        if start > end:
            raise ValueError(f"Invalid range: {start}-{end}")
        
        # Stream file
        async with aiofiles.open(safe_path, mode='rb') as f:
            await f.seek(start)
            remaining = end - start + 1
            
            while remaining > 0:
                chunk_size = min(settings.chunk_size, remaining)
                chunk = await f.read(chunk_size)
                
                if not chunk:
                    break
                
                remaining -= len(chunk)
                yield chunk


# Global file service instance
file_service = FileService()

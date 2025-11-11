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
from app.utils import (
    safe_resolve_path, 
    safe_path_exists, 
    safe_is_file, 
    safe_is_dir,
    safe_stat,
    safe_iterdir,
    normalize_path,
    is_clouddrive_path,
    get_relative_path
)

logger = logging.getLogger(__name__)


class FileService:
    """Service for managing files in CloudDrive2 mount."""
    
    def __init__(self):
        # Use safe path resolution for CloudDrive2 compatibility
        if settings.clouddrive2_compat_mode:
            # Use normpath instead of resolve for virtual filesystems
            self.mount_path = normalize_path(settings.clouddrive_mount_path, use_resolve=False)
            logger.info(f"CloudDrive2 compatibility mode enabled for mount path: {self.mount_path}")
            
            # Detect if this is likely a CloudDrive2 mount
            if is_clouddrive_path(self.mount_path):
                logger.info("CloudDrive2 virtual filesystem detected based on path analysis")
        else:
            # Standard resolution (may fail on CloudDrive2)
            self.mount_path = str(Path(settings.clouddrive_mount_path).resolve())
            logger.info(f"Standard path resolution used for mount path: {self.mount_path}")
        
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
    
    def _get_safe_path(self, relative_path: str) -> str:
        """
        Get safe absolute path within mount directory.
        
        Uses CloudDrive2-compatible path operations that don't rely on
        Path.resolve() which fails on virtual filesystems with OSError [WinError 1005].
        
        SECURITY: This function accepts user-provided paths (by design for file streaming).
        Directory traversal attacks are prevented by:
        1. Normalizing paths to resolve .. and . components (via normalize_path)
        2. Validating the normalized path starts with the mount directory
        3. Raising PermissionError if path escapes mount directory
        
        CodeQL path-injection warnings are expected and safe due to this validation.
        
        Args:
            relative_path: Relative path within mount directory (user-provided)
            
        Returns:
            Safe absolute path as string
            
        Raises:
            PermissionError: If path is outside mount directory (security check)
        """
        # Remove leading slash and construct full path
        clean_path = relative_path.lstrip('/')
        
        if settings.clouddrive2_compat_mode:
            # Use os.path operations for CloudDrive2 compatibility
            full_path = os.path.join(self.mount_path, clean_path)
            # normalize_path resolves .. and . to prevent traversal
            full_path = normalize_path(full_path, use_resolve=False)
            
            # Normalize mount path for comparison (without resolve)
            normalized_mount = normalize_path(self.mount_path, use_resolve=False)
        else:
            # Standard Path.resolve() (may fail on CloudDrive2)
            full_path_obj = Path(self.mount_path) / clean_path
            try:
                # Path.resolve() also resolves .. and . components
                full_path = str(full_path_obj.resolve())
                normalized_mount = str(Path(self.mount_path).resolve())
            except OSError as e:
                # Fallback to CloudDrive2 mode if resolve fails
                logger.warning(
                    f"Path.resolve() failed (CloudDrive2 filesystem?): {e}. "
                    f"Falling back to compatibility mode."
                )
                full_path = os.path.join(self.mount_path, clean_path)
                full_path = normalize_path(full_path, use_resolve=False)
                normalized_mount = normalize_path(self.mount_path, use_resolve=False)
        
        # SECURITY CHECK: Ensure path is within mount directory (prevent directory traversal)
        # Use string comparison for CloudDrive2 compatibility
        full_path_normalized = full_path.replace('\\', '/').rstrip('/')
        mount_normalized = normalized_mount.replace('\\', '/').rstrip('/')
        
        if not full_path_normalized.startswith(mount_normalized):
            raise PermissionError(f"Access denied: path outside mount directory")
        
        return full_path
    
    async def get_file_info(self, file_path: str) -> FileInfo:
        """Get information about a file."""
        safe_path = self._get_safe_path(file_path)
        
        # Use safe path operations for CloudDrive2 compatibility
        if not safe_path_exists(safe_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not safe_is_file(safe_path):
            raise ValueError(f"Path is not a file: {file_path}")
        
        # Get file stats with fallback
        try:
            stat = safe_stat(safe_path)
        except OSError as e:
            logger.error(f"Failed to get stats for {safe_path}: {e}")
            raise
        
        mime_type, _ = mimetypes.guess_type(str(safe_path))
        mime_type = mime_type or 'application/octet-stream'
        
        file_type = self._get_file_type(mime_type)
        
        # Extract extension safely
        path_obj = Path(safe_path)
        extension = path_obj.suffix.lstrip('.')
        
        return FileInfo(
            name=path_obj.name,
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
        
        # Use safe path operations for CloudDrive2 compatibility
        if not safe_path_exists(safe_path):
            raise FileNotFoundError(f"Directory not found: {dir_path}")
        
        if not safe_is_dir(safe_path):
            raise ValueError(f"Path is not a directory: {dir_path}")
        
        files = []
        subdirectories = []
        total_size = 0
        
        # List directory contents with CloudDrive2-safe iteration
        try:
            for entry in safe_iterdir(safe_path):
                try:
                    # Use safe operations for each entry
                    entry_str = str(entry)
                    
                    if safe_is_file(entry_str) and self._is_allowed_file(entry.name):
                        stat = safe_stat(entry_str)
                        mime_type, _ = mimetypes.guess_type(entry_str)
                        mime_type = mime_type or 'application/octet-stream'
                        file_type = self._get_file_type(mime_type)
                        
                        # Create relative path using safe operations
                        try:
                            rel_path = get_relative_path(entry_str, self.mount_path)
                        except ValueError:
                            # Fallback to string operations
                            entry_norm = entry_str.replace('\\', '/')
                            mount_norm = self.mount_path.replace('\\', '/')
                            if entry_norm.startswith(mount_norm):
                                rel_path = entry_norm[len(mount_norm):].lstrip('/')
                            else:
                                logger.warning(f"Cannot compute relative path for {entry_str}")
                                continue
                        
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
                    elif safe_is_dir(entry_str):
                        subdirectories.append(entry.name)
                except (PermissionError, OSError) as e:
                    logger.warning(f"Cannot access {entry}: {e}")
                    continue
        except (PermissionError, OSError) as e:
            logger.error(f"Cannot list directory {safe_path}: {e}")
            raise
        
        # Get directory name safely
        dir_name = os.path.basename(safe_path) or '/'
        
        return DirectoryInfo(
            name=dir_name,
            path=dir_path,
            files=files,
            subdirectories=subdirectories,
            total_files=len(files),
            total_size=total_size
        )
    
    async def get_file_size(self, file_path: str) -> int:
        """Get file size."""
        safe_path = self._get_safe_path(file_path)
        
        # Use safe path operations for CloudDrive2 compatibility
        if not safe_path_exists(safe_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            stat = safe_stat(safe_path)
            return stat.st_size
        except OSError as e:
            logger.error(f"Failed to get file size for {safe_path}: {e}")
            raise
    
    async def stream_file(
        self,
        file_path: str,
        start: int = 0,
        end: Optional[int] = None
    ) -> AsyncGenerator[bytes, None]:
        """
        Stream file content with optional range support.
        
        Supports CloudDrive2 virtual filesystem with safe path operations
        and Range requests for video/audio streaming.
        """
        safe_path = self._get_safe_path(file_path)
        
        # Use safe path operations for CloudDrive2 compatibility
        if not safe_path_exists(safe_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            file_size = safe_stat(safe_path).st_size
        except OSError as e:
            logger.error(f"Failed to get file stats for streaming {safe_path}: {e}")
            raise
        
        # Validate range
        if start < 0 or start >= file_size:
            raise ValueError(f"Invalid start position: {start}")
        
        if end is None:
            end = file_size - 1
        elif end >= file_size:
            end = file_size - 1
        
        if start > end:
            raise ValueError(f"Invalid range: {start}-{end}")
        
        # Stream file with CloudDrive2 compatibility
        try:
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
        except OSError as e:
            logger.error(f"Error streaming file {safe_path}: {e}")
            raise


# Global file service instance
file_service = FileService()

"""Utility functions for safe path operations with CloudDrive2 compatibility.

SECURITY NOTE: Functions in this module accept user-provided paths by design,
as this is a file streaming service. Path injection warnings from CodeQL are
expected. Security is maintained through:

1. Path normalization (resolves .. and . components)
2. Validation in FileService._get_safe_path() that ensures paths stay within mount
3. No execution of user paths - only file read operations

The path operations in this module are safe wrappers that:
- Provide CloudDrive2 virtual filesystem compatibility
- Fall back to os.path operations when Path methods fail
- Do not introduce security vulnerabilities when used with proper validation
"""
import os
import logging
from pathlib import Path
from typing import Union, Optional

logger = logging.getLogger(__name__)


def safe_resolve_path(path: Union[str, Path], fallback_to_normpath: bool = True) -> str:
    """
    Safely resolve a path with CloudDrive2 virtual filesystem compatibility.
    
    CloudDrive2 mounts create virtual filesystems on Windows that don't support
    GetFinalPathNameByHandle() used by Path.resolve(), causing OSError [WinError 1005].
    
    Args:
        path: Path to resolve (can be string or Path object)
        fallback_to_normpath: If True, falls back to os.path.normpath on OSError
        
    Returns:
        Resolved path as string
        
    Raises:
        OSError: If path resolution fails and fallback is disabled
    """
    try:
        # Try standard Path.resolve() first
        if isinstance(path, str):
            path = Path(path)
        resolved = path.resolve()
        return str(resolved)
    except OSError as e:
        # CloudDrive2 virtual filesystem compatibility
        if fallback_to_normpath:
            logger.debug(
                f"Path.resolve() failed for {path} (CloudDrive2 virtual filesystem?): {e}. "
                f"Falling back to os.path.normpath()"
            )
            # Use os.path.normpath for CloudDrive2 compatibility
            normalized = os.path.normpath(os.path.abspath(str(path)))
            return normalized
        else:
            raise


def safe_path_exists(path: Union[str, Path]) -> bool:
    """
    Safely check if a path exists with exception handling.
    
    Args:
        path: Path to check
        
    Returns:
        True if path exists, False otherwise
    """
    try:
        if isinstance(path, str):
            path = Path(path)
        return path.exists()
    except OSError as e:
        logger.warning(f"Error checking if path exists {path}: {e}")
        # Fallback to os.path.exists for virtual filesystems
        try:
            return os.path.exists(str(path))
        except Exception as e2:
            logger.error(f"Fallback path.exists also failed for {path}: {e2}")
            return False


def safe_is_file(path: Union[str, Path]) -> bool:
    """
    Safely check if a path is a file with exception handling.
    
    Args:
        path: Path to check
        
    Returns:
        True if path is a file, False otherwise
    """
    try:
        if isinstance(path, str):
            path = Path(path)
        return path.is_file()
    except OSError as e:
        logger.warning(f"Error checking if path is file {path}: {e}")
        # Fallback to os.path.isfile for virtual filesystems
        try:
            return os.path.isfile(str(path))
        except Exception as e2:
            logger.error(f"Fallback isfile also failed for {path}: {e2}")
            return False


def safe_is_dir(path: Union[str, Path]) -> bool:
    """
    Safely check if a path is a directory with exception handling.
    
    Args:
        path: Path to check
        
    Returns:
        True if path is a directory, False otherwise
    """
    try:
        if isinstance(path, str):
            path = Path(path)
        return path.is_dir()
    except OSError as e:
        logger.warning(f"Error checking if path is directory {path}: {e}")
        # Fallback to os.path.isdir for virtual filesystems
        try:
            return os.path.isdir(str(path))
        except Exception as e2:
            logger.error(f"Fallback isdir also failed for {path}: {e2}")
            return False


def safe_stat(path: Union[str, Path]):
    """
    Safely get file stats with exception handling.
    
    Args:
        path: Path to stat
        
    Returns:
        os.stat_result object
        
    Raises:
        OSError: If stat fails
    """
    try:
        if isinstance(path, str):
            path = Path(path)
        return path.stat()
    except OSError as e:
        logger.debug(f"Path.stat() failed for {path}, trying os.stat(): {e}")
        # Fallback to os.stat for virtual filesystems
        return os.stat(str(path))


def safe_iterdir(path: Union[str, Path]):
    """
    Safely iterate directory contents with exception handling.
    
    Args:
        path: Directory path to iterate
        
    Yields:
        Path objects for directory contents
        
    Raises:
        OSError: If directory iteration fails
    """
    try:
        if isinstance(path, str):
            path = Path(path)
        
        # Try Path.iterdir() first
        for entry in path.iterdir():
            yield entry
    except OSError as e:
        logger.debug(f"Path.iterdir() failed for {path}, trying os.listdir(): {e}")
        # Fallback to os.listdir for virtual filesystems
        try:
            for name in os.listdir(str(path)):
                yield Path(path) / name
        except Exception as e2:
            logger.error(f"Failed to iterate directory {path}: {e2}")
            raise


def normalize_path(path: Union[str, Path], use_resolve: bool = False) -> str:
    """
    Normalize a path using the most compatible method.
    
    For CloudDrive2 compatibility, defaults to os.path.normpath instead of Path.resolve().
    This function properly handles .. and . components while avoiding Path.resolve().
    
    Args:
        path: Path to normalize
        use_resolve: If True, attempts to use Path.resolve() with fallback
        
    Returns:
        Normalized path as string
    """
    path_str = str(path)
    
    if use_resolve:
        return safe_resolve_path(path_str, fallback_to_normpath=True)
    else:
        # Direct normpath for best CloudDrive2 compatibility
        # First make it absolute, then normalize to resolve .. and .
        abs_path = os.path.abspath(path_str)
        normalized = os.path.normpath(abs_path)
        return normalized


def is_clouddrive_path(path: Union[str, Path]) -> bool:
    """
    Detect if a path is likely a CloudDrive2 virtual filesystem mount.
    
    This is a heuristic check based on common CloudDrive2 mount patterns.
    
    Args:
        path: Path to check
        
    Returns:
        True if path appears to be a CloudDrive2 mount
    """
    path_str = str(path).lower()
    
    # Common CloudDrive2 mount point patterns
    clouddrive_indicators = [
        'clouddrive',
        'cd2',
        'googledrive',
        'gdrive'
    ]
    
    for indicator in clouddrive_indicators:
        if indicator in path_str:
            return True
    
    # Check if Path.resolve() fails (strong indicator of virtual filesystem)
    try:
        if isinstance(path, str):
            path = Path(path)
        path.resolve()
        return False
    except OSError:
        logger.info(f"Path.resolve() failed for {path}, treating as CloudDrive2 virtual filesystem")
        return True


def get_relative_path(path: Union[str, Path], base: Union[str, Path]) -> str:
    """
    Get relative path from base, with CloudDrive2 compatibility.
    
    Args:
        path: Full path
        base: Base path
        
    Returns:
        Relative path as string
    """
    try:
        # Try standard relative_to first
        if isinstance(path, str):
            path = Path(path)
        if isinstance(base, str):
            base = Path(base)
        
        rel = path.relative_to(base)
        return str(rel)
    except (ValueError, OSError) as e:
        logger.debug(f"Path.relative_to() failed, using string operations: {e}")
        # Fallback to string-based operations
        path_str = normalize_path(path, use_resolve=False)
        base_str = normalize_path(base, use_resolve=False)
        
        # Ensure both use same separator
        path_str = path_str.replace('\\', '/')
        base_str = base_str.replace('\\', '/')
        
        # Remove base from path
        if path_str.startswith(base_str):
            rel_path = path_str[len(base_str):].lstrip('/')
            return rel_path
        else:
            raise ValueError(f"Path {path} is not relative to {base}")

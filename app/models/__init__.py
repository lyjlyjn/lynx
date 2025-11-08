"""Data models for the application."""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class FileType(str, Enum):
    """File type enumeration."""
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    OTHER = "other"


class FileInfo(BaseModel):
    """File information model."""
    name: str
    path: str
    size: int
    type: FileType
    extension: str
    modified: datetime
    mime_type: str
    is_streamable: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "movie.mp4",
                "path": "/videos/movie.mp4",
                "size": 1024000000,
                "type": "video",
                "extension": "mp4",
                "modified": "2024-01-01T12:00:00",
                "mime_type": "video/mp4",
                "is_streamable": True
            }
        }


class DirectoryInfo(BaseModel):
    """Directory information model."""
    name: str
    path: str
    files: List[FileInfo] = []
    subdirectories: List[str] = []
    total_files: int = 0
    total_size: int = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "videos",
                "path": "/videos",
                "files": [],
                "subdirectories": ["movies", "tv-shows"],
                "total_files": 10,
                "total_size": 10240000000
            }
        }


class StreamInfo(BaseModel):
    """Stream information model."""
    file_path: str
    file_size: int
    content_type: str
    supports_range: bool = True
    chunk_size: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "file_path": "/videos/movie.mp4",
                "file_size": 1024000000,
                "content_type": "video/mp4",
                "supports_range": True,
                "chunk_size": 1048576
            }
        }


class MediaMetadata(BaseModel):
    """Media file metadata."""
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    bitrate: Optional[int] = None
    codec: Optional[str] = None
    format: Optional[str] = None
    audio_codec: Optional[str] = None
    audio_channels: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "duration": 7200.5,
                "width": 1920,
                "height": 1080,
                "bitrate": 5000000,
                "codec": "h264",
                "format": "mp4",
                "audio_codec": "aac",
                "audio_channels": 2
            }
        }


class TokenResponse(BaseModel):
    """Authentication token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "File not found",
                "status_code": 404,
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2024-01-01T12:00:00"
            }
        }

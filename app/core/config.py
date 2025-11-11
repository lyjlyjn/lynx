"""Application configuration using pydantic-settings."""
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = Field(default="CloudDrive2 Media Streaming", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # CloudDrive2
    clouddrive_mount_path: str = Field(default="/mnt/clouddrive", env="CLOUDDRIVE_MOUNT_PATH")
    allowed_extensions: str = Field(
        default="mp4,mkv,avi,mov,wmv,flv,webm,mp3,wav,flac,aac,ogg,m4a,pdf,doc,docx,txt,epub",
        env="ALLOWED_EXTENSIONS"
    )
    
    # Security
    secret_key: str = Field(
        default="change-this-secret-key-in-production",
        env="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Authentication (optional)
    auth_username: Optional[str] = Field(default=None, env="AUTH_USERNAME")
    auth_password: Optional[str] = Field(default=None, env="AUTH_PASSWORD")
    
    # Cache
    cache_enabled: bool = Field(default=True, env="CACHE_ENABLED")
    cache_ttl: int = Field(default=300, env="CACHE_TTL")
    cache_max_size: int = Field(default=1000, env="CACHE_MAX_SIZE")
    
    # Streaming
    chunk_size: int = Field(default=1024 * 1024, env="CHUNK_SIZE")  # 1MB
    max_chunk_size: int = Field(default=10 * 1024 * 1024, env="MAX_CHUNK_SIZE")  # 10MB
    buffer_size: int = Field(default=65536, env="BUFFER_SIZE")  # 64KB
    enable_range_requests: bool = Field(default=True, env="ENABLE_RANGE_REQUESTS")
    
    # Performance
    max_workers: int = Field(default=4, env="MAX_WORKERS")
    keep_alive_timeout: int = Field(default=75, env="KEEP_ALIVE_TIMEOUT")
    
    # CORS
    cors_origins: str = Field(default="*", env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: str = Field(default="*", env="CORS_ALLOW_METHODS")
    cors_allow_headers: str = Field(default="*", env="CORS_ALLOW_HEADERS")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/app.log", env="LOG_FILE")
    
    # Redis (optional)
    redis_host: Optional[str] = Field(default=None, env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    
    # CloudDrive2 Virtual Filesystem Compatibility
    clouddrive2_compat_mode: bool = Field(
        default=True, 
        env="CLOUDDRIVE2_COMPAT_MODE",
        description="Enable CloudDrive2 virtual filesystem compatibility. "
                    "When enabled, uses os.path.normpath instead of Path.resolve() "
                    "to avoid OSError [WinError 1005] on Windows virtual filesystems."
    )
    filesystem_fallback_enabled: bool = Field(
        default=True,
        env="FILESYSTEM_FALLBACK_ENABLED",
        description="Enable fallback to os.path operations when Path methods fail. "
                    "Recommended for CloudDrive2 and other virtual filesystems."
    )
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Get allowed extensions as a list."""
        return [ext.strip() for ext in self.allowed_extensions.split(',')]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(',')]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

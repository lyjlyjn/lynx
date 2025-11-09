"""Media metadata extraction service."""
import logging
import subprocess
import json
from typing import Optional
from pathlib import Path

from app.models import MediaMetadata
from app.core.config import settings

logger = logging.getLogger(__name__)


class MediaService:
    """Service for extracting media metadata using ffprobe."""
    
    async def get_metadata(self, file_path: str) -> Optional[MediaMetadata]:
        """Extract metadata from media file using ffprobe."""
        try:
            # Try to get metadata using ffprobe
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                file_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                logger.warning(f"ffprobe failed for {file_path}: {result.stderr}")
                return None
            
            data = json.loads(result.stdout)
            
            # Extract video stream info
            video_stream = next(
                (s for s in data.get('streams', []) if s.get('codec_type') == 'video'),
                None
            )
            
            # Extract audio stream info
            audio_stream = next(
                (s for s in data.get('streams', []) if s.get('codec_type') == 'audio'),
                None
            )
            
            # Extract format info
            format_info = data.get('format', {})
            
            metadata = MediaMetadata(
                duration=float(format_info.get('duration', 0)) if format_info.get('duration') else None,
                bitrate=int(format_info.get('bit_rate', 0)) if format_info.get('bit_rate') else None,
                format=format_info.get('format_name'),
            )
            
            if video_stream:
                metadata.width = video_stream.get('width')
                metadata.height = video_stream.get('height')
                metadata.codec = video_stream.get('codec_name')
            
            if audio_stream:
                metadata.audio_codec = audio_stream.get('codec_name')
                metadata.audio_channels = audio_stream.get('channels')
            
            return metadata
            
        except subprocess.TimeoutExpired:
            logger.warning(f"ffprobe timeout for {file_path}")
            return None
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse ffprobe output for {file_path}: {e}")
            return None
        except FileNotFoundError:
            logger.warning("ffprobe not found - media metadata extraction disabled")
            return None
        except Exception as e:
            logger.error(f"Error extracting metadata for {file_path}: {e}")
            return None


# Global media service instance
media_service = MediaService()

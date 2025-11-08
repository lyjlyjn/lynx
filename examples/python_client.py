#!/usr/bin/env python3
"""
Example Python client for CloudDrive2 Media Streaming API.

This client demonstrates:
- Authentication with the API
- Listing files and directories
- Downloading files with Range request support
- Resumable downloads
"""

import requests
from typing import Optional
import os


class CloudDriveClient:
    """Client for CloudDrive2 Media Streaming API."""
    
    def __init__(self, base_url: str, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the client.
        
        Args:
            base_url: Base URL of the streaming service
            username: Optional username for authentication
            password: Optional password for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.auth = (username, password) if username and password else None
        self.session = requests.Session()
        
    def list_directory(self, path: str = "/") -> dict:
        """
        List contents of a directory.
        
        Args:
            path: Directory path to list
            
        Returns:
            Dictionary with directory information
        """
        url = f"{self.base_url}/api/files/list{path if path != '/' else ''}"
        response = self.session.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def get_file_info(self, file_path: str) -> dict:
        """
        Get information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        url = f"{self.base_url}/api/files/info{file_path}"
        response = self.session.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def get_stream_info(self, file_path: str) -> dict:
        """
        Get streaming information for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with stream information
        """
        url = f"{self.base_url}/api/stream{file_path}/info"
        response = self.session.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def get_media_metadata(self, file_path: str) -> Optional[dict]:
        """
        Get media metadata for a video/audio file.
        
        Args:
            file_path: Path to the media file
            
        Returns:
            Dictionary with metadata or None
        """
        url = f"{self.base_url}/api/stream{file_path}/metadata"
        response = self.session.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def download_file(
        self,
        file_path: str,
        output_path: str,
        resume: bool = True,
        chunk_size: int = 1024 * 1024
    ):
        """
        Download a file with support for resuming.
        
        Args:
            file_path: Path to the file on the server
            output_path: Local path to save the file
            resume: Whether to resume partial downloads
            chunk_size: Size of chunks to download
        """
        url = f"{self.base_url}/api/stream{file_path}"
        
        # Check if file exists and get current size
        start_byte = 0
        mode = 'wb'
        
        if resume and os.path.exists(output_path):
            start_byte = os.path.getsize(output_path)
            mode = 'ab'
        
        # Get file info
        file_info = self.get_file_info(file_path)
        total_size = file_info['size']
        
        if start_byte >= total_size:
            print(f"File already downloaded: {output_path}")
            return
        
        # Prepare headers for Range request
        headers = {}
        if start_byte > 0:
            headers['Range'] = f'bytes={start_byte}-'
            print(f"Resuming download from byte {start_byte}")
        
        # Download file
        response = self.session.get(url, auth=self.auth, headers=headers, stream=True)
        response.raise_for_status()
        
        downloaded = start_byte
        with open(output_path, mode) as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress = (downloaded / total_size) * 100
                    print(f"\rProgress: {progress:.1f}% ({downloaded}/{total_size} bytes)", end='')
        
        print(f"\nDownload complete: {output_path}")
    
    def stream_url(self, file_path: str) -> str:
        """
        Get the streaming URL for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Full URL for streaming
        """
        return f"{self.base_url}/api/stream{file_path}"


def main():
    """Example usage."""
    # Initialize client
    client = CloudDriveClient(
        base_url="http://localhost:8000",
        username=None,  # Set if authentication is enabled
        password=None
    )
    
    # List root directory
    print("Listing root directory:")
    root_contents = client.list_directory("/")
    print(f"Files: {root_contents['total_files']}")
    print(f"Subdirectories: {root_contents['subdirectories']}")
    print()
    
    # List files in root
    if root_contents['files']:
        print("Files in root:")
        for file in root_contents['files'][:5]:  # Show first 5 files
            print(f"  - {file['name']} ({file['size']} bytes, {file['type']})")
        print()
    
    # Example: Download a file (commented out)
    # client.download_file("/videos/movie.mp4", "downloaded_movie.mp4", resume=True)
    
    # Example: Get streaming URL
    # stream_url = client.stream_url("/videos/movie.mp4")
    # print(f"Streaming URL: {stream_url}")


if __name__ == "__main__":
    main()

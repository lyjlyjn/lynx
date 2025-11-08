#!/usr/bin/env python3
"""
Test script for CloudDrive2 Media Streaming Application.
"""

import sys
import os
from pathlib import Path

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from app.core import settings
        print(f"✓ Settings loaded: {settings.app_name}")
        
        from app.models import FileInfo, DirectoryInfo, StreamInfo
        print("✓ Models imported")
        
        from app.services import file_service, cache_service, media_service
        print("✓ Services imported")
        
        from app.api import api_router
        print("✓ API router imported")
        
        from app.main import app
        print("✓ Main app imported")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from app.core import settings
        
        print(f"  App name: {settings.app_name}")
        print(f"  Version: {settings.app_version}")
        print(f"  Mount path: {settings.clouddrive_mount_path}")
        print(f"  Chunk size: {settings.chunk_size}")
        print(f"  Range requests: {settings.enable_range_requests}")
        print(f"  Allowed extensions: {len(settings.allowed_extensions_list)} types")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_app_creation():
    """Test FastAPI app creation."""
    print("\nTesting app creation...")
    
    try:
        from app.main import app
        
        print(f"  App title: {app.title}")
        print(f"  App version: {app.version}")
        print(f"  Routes count: {len(app.routes)}")
        
        # List some routes
        print("  Sample routes:")
        for route in list(app.routes)[:10]:
            if hasattr(route, 'path'):
                print(f"    {route.path}")
        
        return True
    except Exception as e:
        print(f"✗ App creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_services():
    """Test service initialization."""
    print("\nTesting services...")
    
    try:
        from app.services import file_service, cache_service
        
        print(f"  File service mount path: {file_service.mount_path}")
        print(f"  File service allowed extensions: {len(file_service.allowed_extensions)}")
        print(f"  Cache service enabled: {cache_service.enabled}")
        print(f"  Cache service stats: {cache_service.get_stats()}")
        
        return True
    except Exception as e:
        print(f"✗ Services test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("CloudDrive2 Media Streaming - Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_configuration()))
    results.append(("App Creation", test_app_creation()))
    results.append(("Services", test_services()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("=" * 60)
    if all_passed:
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed! ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())

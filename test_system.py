#!/usr/bin/env python
"""
Test script to verify Face Recognition System is properly set up
"""

import sys
from pathlib import Path
import subprocess

def test_python_version():
    """Test Python version"""
    print("\n✓ Testing Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (need 3.8+)")
        return False

def test_csv_file():
    """Test if CSV file exists"""
    print("✓ Testing CSV file...", end=" ")
    csv_path = Path("StudentPicsDataset.csv")
    if csv_path.exists():
        import pandas as pd
        try:
            df = pd.read_csv(csv_path)
            print(f"✅ Found with {len(df)} rows")
            return True
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
            return False
    else:
        print(f"❌ StudentPicsDataset.csv not found")
        return False

def test_dependencies():
    """Test if all dependencies are installed"""
    print("✓ Testing dependencies...")
    
    dependencies = {
        'cv2': 'opencv-python',
        'deepface': 'deepface',
        'tensorflow': 'tensorflow',
        'keras': 'keras',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'PIL': 'pillow',
        'requests': 'requests'
    }
    
    all_ok = True
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED")
            all_ok = False
    
    return all_ok

def test_camera():
    """Test if camera is accessible"""
    print("\n✓ Testing camera access...", end=" ")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap.release()
            print("✅ Camera is accessible")
            return True
        else:
            print("❌ Camera not found or not accessible")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_google_drive_downloader():
    """Test Google Drive downloader module"""
    print("✓ Testing GoogleDriveDownloader module...", end=" ")
    try:
        from google_drive_downloader import GoogleDriveDownloader
        print("✅ Module loads correctly")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_face_recognizer():
    """Test Face Recognizer module"""
    print("✓ Testing FaceRecognizer module...", end=" ")
    try:
        from face_recognizer import FaceRecognizer
        print("✅ Module loads correctly")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_main_app():
    """Test main application module"""
    print("✓ Testing main application...", end=" ")
    try:
        from main import CameraFaceRecognition
        print("✅ Module loads correctly")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_config():
    """Test configuration file"""
    print("✓ Testing configuration file...", end=" ")
    config_path = Path("config.json")
    if config_path.exists():
        try:
            import json
            with open(config_path, 'r') as f:
                json.load(f)
            print("✅ Config file is valid")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print("⚠️ Config file not found (optional)")
        return True

def test_directories():
    """Test if necessary directories can be created"""
    print("✓ Testing directory creation...", end=" ")
    try:
        Path("student_photos").mkdir(exist_ok=True)
        Path("screenshots").mkdir(exist_ok=True)
        print("✅ Directories ready")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("🧪 FACE RECOGNITION SYSTEM - DIAGNOSTIC TEST")
    print("=" * 70)
    
    tests = [
        ("Python Version", test_python_version),
        ("CSV File", test_csv_file),
        ("Dependencies", test_dependencies),
        ("Camera Access", test_camera),
        ("Directory Structure", test_directories),
        ("Google Drive Module", test_google_drive_downloader),
        ("Face Recognizer Module", test_face_recognizer),
        ("Main Application", test_main_app),
        ("Configuration", test_config),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n⚠️ Unexpected error in {test_name}: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed! You can run the system with: python main.py")
    elif passed >= total - 1:
        print("\n⚠️ Most tests passed, but fix the failing tests before running.")
    else:
        print("\n❌ Several tests failed. Please run setup: python setup.py")
    
    print("=" * 70 + "\n")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

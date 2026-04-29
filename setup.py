import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install all required Python packages"""
    print("📦 Installing required packages...")
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False
    
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_csv():
    """Check if CSV file exists"""
    csv_path = Path("StudentPicsDataset.csv")
    if csv_path.exists():
        print(f"✅ CSV file found: {csv_path}")
        return True
    else:
        print(f"❌ CSV file not found: {csv_path}")
        print("   Please ensure StudentPicsDataset.csv is in the project directory")
        return False

def check_camera():
    """Check if camera is accessible"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap.release()
            print("✅ Camera is accessible")
            return True
        else:
            print("⚠️ Warning: Camera might not be accessible")
            return False
    except Exception as e:
        print(f"⚠️ Could not test camera: {e}")
        return False

if __name__ == "__main__":
    print("\n🚀 Face Recognition System Setup")
    print("=" * 70)
    
    # Check CSV
    if not check_csv():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check camera
    check_camera()
    
    print("\n" + "=" * 70)
    print("✅ Setup complete! You can now run: python main.py")
    print("=" * 70)

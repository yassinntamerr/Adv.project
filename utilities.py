#!/usr/bin/env python
"""
Utility script for face recognition system management
Provides various helper functions
"""

import json
from pathlib import Path
import pandas as pd
from google_drive_downloader import GoogleDriveDownloader
from face_recognizer import FaceRecognizer
import sys

def validate_csv():
    """Validate the CSV file"""
    csv_path = Path("StudentPicsDataset.csv")
    
    print("\n📋 CSV Validation")
    print("=" * 70)
    
    if not csv_path.exists():
        print("❌ CSV file not found!")
        return False
    
    try:
        df = pd.read_csv(csv_path)
        
        print(f"✅ CSV file found")
        print(f"   - Total rows: {len(df)}")
        print(f"   - Columns: {', '.join(df.columns)}")
        
        # Check required columns
        required_cols = ['Student ID', 'Student Name', 'Photo Link']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            print(f"❌ Missing columns: {', '.join(missing)}")
            return False
        
        # Check for valid data
        valid_rows = 0
        invalid_rows = 0
        
        for _, row in df.iterrows():
            if pd.notna(row['Student ID']) and pd.notna(row['Student Name']) and pd.notna(row['Photo Link']):
                valid_rows += 1
            else:
                invalid_rows += 1
        
        print(f"   - Valid student records: {valid_rows}")
        print(f"   - Empty/invalid records: {invalid_rows}")
        
        if valid_rows == 0:
            print("❌ No valid student records found!")
            return False
        
        print("\n✅ CSV validation passed!")
        return True
    
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return False

def download_photos(csv_path="StudentPicsDataset.csv"):
    """Download all student photos"""
    print("\n📥 Downloading Photos")
    print("=" * 70)
    
    try:
        downloader = GoogleDriveDownloader(csv_path)
        photos_index = downloader.download_all_photos()
        
        print(f"\n✅ Download complete!")
        print(f"   Total photos downloaded: {len(photos_index)}")
        return photos_index
    
    except Exception as e:
        print(f"❌ Error downloading photos: {e}")
        return None

def prepare_embeddings(photos_index):
    """Prepare face embeddings"""
    print("\n🧠 Preparing Face Embeddings")
    print("=" * 70)
    
    try:
        recognizer = FaceRecognizer(photos_index)
        
        print(f"\n✅ Embeddings prepared!")
        print(f"   Total embeddings prepared: {len(recognizer.known_embeddings)}")
        return recognizer
    
    except Exception as e:
        print(f"❌ Error preparing embeddings: {e}")
        return None

def get_system_info():
    """Get system information"""
    print("\n📊 System Information")
    print("=" * 70)
    
    # Python version
    import sys
    print(f"Python Version: {sys.version}")
    
    # CSV info
    csv_path = Path("StudentPicsDataset.csv")
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        valid_count = df[df['Student ID'].notna()].shape[0]
        print(f"CSV Records: {valid_count}")
    
    # Photos directory
    photos_dir = Path("student_photos")
    if photos_dir.exists():
        photo_count = len(list(photos_dir.glob("*.jpg")))
        print(f"Downloaded Photos: {photo_count}")
    
    # Logs
    log_file = Path("recognition_log.json")
    if log_file.exists():
        with open(log_file, 'r') as f:
            log_count = sum(1 for _ in f)
        print(f"Recognition Events Logged: {log_count}")
    
    # Screenshots
    screenshots_dir = Path("screenshots")
    if screenshots_dir.exists():
        ss_count = len(list(screenshots_dir.glob("*.jpg")))
        print(f"Screenshots Saved: {ss_count}")

def clean_cache():
    """Clean downloaded photos and cache"""
    print("\n🗑️  Cleaning Cache")
    print("=" * 70)
    
    import shutil
    
    photos_dir = Path("student_photos")
    if photos_dir.exists():
        try:
            shutil.rmtree(photos_dir)
            print("✅ Cleaned downloaded photos")
        except Exception as e:
            print(f"❌ Error cleaning photos: {e}")

def export_student_list(output_file="student_list.csv"):
    """Export student list from CSV"""
    print(f"\n📤 Exporting Student List")
    print("=" * 70)
    
    csv_path = Path("StudentPicsDataset.csv")
    if not csv_path.exists():
        print("❌ CSV file not found!")
        return
    
    try:
        df = pd.read_csv(csv_path)
        
        # Keep only valid records
        df = df[df['Student ID'].notna() & df['Student Name'].notna()]
        
        # Create export dataframe
        export_df = df[['Student ID', 'Student Name']].copy()
        export_df = export_df.drop_duplicates(subset=['Student ID'])
        
        export_df.to_csv(output_file, index=False)
        print(f"✅ Exported {len(export_df)} unique students to {output_file}")
    
    except Exception as e:
        print(f"❌ Error exporting: {e}")

def show_menu():
    """Show menu options"""
    print("\n" + "=" * 70)
    print("🔧 FACE RECOGNITION SYSTEM UTILITIES")
    print("=" * 70)
    print("""
1. Validate CSV file
2. Download all photos
3. Prepare face embeddings
4. Get system information
5. Export student list
6. Clean cache
7. Run diagnostics (test_system.py)
8. Analyze logs (analyze_logs.py)
9. Exit

Enter your choice (1-9):
""")

def main():
    """Main menu"""
    while True:
        show_menu()
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            validate_csv()
        
        elif choice == '2':
            photos_index = download_photos()
            if photos_index:
                print(f"\n✅ Downloaded {len(photos_index)} photos")
        
        elif choice == '3':
            csv_path = "StudentPicsDataset.csv"
            downloader = GoogleDriveDownloader(csv_path)
            photos_index = downloader.get_photos_index()
            
            if photos_index:
                recognizer = prepare_embeddings(photos_index)
                if recognizer:
                    print(f"✅ System ready to recognize {len(recognizer.known_embeddings)} students")
        
        elif choice == '4':
            get_system_info()
        
        elif choice == '5':
            export_student_list()
        
        elif choice == '6':
            response = input("Are you sure? This will delete all cached photos (y/n): ")
            if response.lower() == 'y':
                clean_cache()
        
        elif choice == '7':
            print("\nRunning diagnostics...")
            import subprocess
            subprocess.call([sys.executable, "test_system.py"])
        
        elif choice == '8':
            print("\nAnalyzing logs...")
            import subprocess
            subprocess.call([sys.executable, "analyze_logs.py"])
        
        elif choice == '9':
            print("\n✅ Goodbye!")
            break
        
        else:
            print("❌ Invalid option. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

import os
import requests
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import re

class GoogleDriveDownloader:
    """Download images from Google Drive links and manage the dataset"""
    
    def __init__(self, csv_path, output_dir="student_photos"):
        """
        Initialize the downloader
        
        Args:
            csv_path: Path to the CSV file with student data
            output_dir: Directory to store downloaded photos
        """
        self.csv_path = csv_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.df = pd.read_csv(csv_path)
        self.photos_index = {}  # Store mapping of student_id to photo path
        
    def extract_file_id(self, url):
        """Extract file ID from Google Drive URL"""
        # Handle different Google Drive URL formats
        match = re.search(r'id=([a-zA-Z0-9-_]+)', url)
        if match:
            return match.group(1)
        return None
    
    def download_photo(self, student_id, student_name, drive_url, retry=3):
        """
        Download a single photo from Google Drive
        
        Args:
            student_id: Student ID
            student_name: Student name
            drive_url: Google Drive URL
            retry: Number of retries if download fails
            
        Returns:
            Path to downloaded photo or None if failed
        """
        if pd.isna(drive_url) or drive_url == '':
            return None
            
        file_id = self.extract_file_id(drive_url)
        if not file_id:
            print(f"❌ Could not extract file ID from URL: {drive_url}")
            return None
        
        # Create filename
        safe_name = student_name.replace('/', '_').replace('\\', '_')[:50]
        filename = f"{student_id}_{safe_name}.jpg"
        filepath = self.output_dir / filename
        
        # Skip if already downloaded
        if filepath.exists():
            return str(filepath)
        
        # Download the file
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
        for attempt in range(retry):
            try:
                response = requests.get(download_url, timeout=10)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    return str(filepath)
            except Exception as e:
                if attempt == retry - 1:
                    print(f"❌ Failed to download for {student_name} (ID: {student_id}): {e}")
                    return None
                continue
        
        return None
    
    def download_all_photos(self):
        """Download all photos from the CSV file"""
        print(f"\n📥 Starting to download {len(self.df)} student photos...")
        
        successful = 0
        failed = 0
        
        for idx, row in tqdm(self.df.iterrows(), total=len(self.df), desc="Downloading photos"):
            student_id = row.get('Student ID')
            student_name = row.get('Student Name')
            photo_link = row.get('Photo Link')
            
            # Skip empty rows
            if pd.isna(student_id) or pd.isna(student_name) or pd.isna(photo_link):
                continue
            
            filepath = self.download_photo(str(student_id), student_name, photo_link)
            
            if filepath:
                self.photos_index[str(student_id)] = {
                    'name': student_name,
                    'path': filepath
                }
                successful += 1
            else:
                failed += 1
        
        print(f"\n✅ Download complete! Successful: {successful}, Failed: {failed}")
        return self.photos_index
    
    def get_photos_index(self):
        """Get the index of downloaded photos"""
        if not self.photos_index:
            self.download_all_photos()
        return self.photos_index
    
    def get_student_name(self, student_id):
        """Get student name by ID"""
        if student_id in self.photos_index:
            return self.photos_index[student_id]['name']
        return None
    
    def get_student_photo_path(self, student_id):
        """Get photo path for a student ID"""
        if student_id in self.photos_index:
            return self.photos_index[student_id]['path']
        return None


if __name__ == "__main__":
    # Test the downloader
    csv_path = "StudentPicsDataset.csv"
    downloader = GoogleDriveDownloader(csv_path)
    index = downloader.download_all_photos()
    print(f"\n📊 Total photos downloaded: {len(index)}")

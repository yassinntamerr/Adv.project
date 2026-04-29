import cv2
import numpy as np
from pathlib import Path
from deepface import DeepFace
from tqdm import tqdm
import pandas as pd

class FaceRecognizer:
    """Face recognition system using DeepFace"""
    
    def __init__(self, photos_index):
        """
        Initialize the face recognizer
        
        Args:
            photos_index: Dictionary of student_id -> {'name': name, 'path': photo_path}
        """
        self.photos_index = photos_index
        self.known_embeddings = {}  # Store embeddings for known faces
        self.model = "VGGFace2"  # DeepFace model to use
        self.distance_threshold = 0.6  # Threshold for face matching
        
        print("🧠 Initializing face recognition model...")
        self._prepare_known_embeddings()
    
    def _prepare_known_embeddings(self):
        """Prepare embeddings for all known student photos"""
        print("\n🔄 Preparing embeddings for known faces...")
        
        for student_id, info in tqdm(self.photos_index.items(), desc="Processing student photos"):
            try:
                photo_path = info['path']
                if not Path(photo_path).exists():
                    continue
                
                # Get face embedding using DeepFace
                embedding = DeepFace.represent(
                    img_path=photo_path,
                    model_name=self.model,
                    enforce_detection=False
                )
                
                if embedding:
                    self.known_embeddings[student_id] = {
                        'embedding': embedding[0]['embedding'],
                        'name': info['name']
                    }
            except Exception as e:
                print(f"⚠️ Could not process photo for {info['name']}: {str(e)[:50]}")
                continue
        
        print(f"✅ Prepared embeddings for {len(self.known_embeddings)} students")
    
    def recognize_face_in_image(self, image_path, confidence_threshold=0.6):
        """
        Recognize faces in an image file
        
        Args:
            image_path: Path to the image file
            confidence_threshold: Minimum confidence for a match
            
        Returns:
            List of tuples: (student_id, student_name, confidence)
        """
        try:
            # Get face embedding from the image
            embedding = DeepFace.represent(
                img_path=image_path,
                model_name=self.model,
                enforce_detection=False
            )
            
            if not embedding:
                return []
            
            captured_embedding = embedding[0]['embedding']
            results = []
            
            # Compare with all known embeddings
            for student_id, known_info in self.known_embeddings.items():
                distance = self._euclidean_distance(
                    captured_embedding,
                    known_info['embedding']
                )
                
                # Convert distance to confidence (0-1 scale, lower distance = higher confidence)
                confidence = 1 / (1 + distance)
                
                if confidence >= confidence_threshold:
                    results.append((student_id, known_info['name'], confidence))
            
            # Sort by confidence (descending)
            results.sort(key=lambda x: x[2], reverse=True)
            return results
        
        except Exception as e:
            print(f"❌ Error recognizing face: {str(e)}")
            return []
    
    def recognize_face_in_frame(self, frame, confidence_threshold=0.6):
        """
        Recognize faces in a video frame
        
        Args:
            frame: OpenCV frame/image
            confidence_threshold: Minimum confidence for a match
            
        Returns:
            List of tuples: (student_id, student_name, confidence, face_location)
        """
        try:
            # Convert frame to RGB (DeepFace expects RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get face embedding from the frame
            embedding = DeepFace.represent(
                img_path=rgb_frame,
                model_name=self.model,
                enforce_detection=False
            )
            
            if not embedding:
                return []
            
            captured_embedding = embedding[0]['embedding']
            results = []
            
            # Compare with all known embeddings
            for student_id, known_info in self.known_embeddings.items():
                distance = self._euclidean_distance(
                    captured_embedding,
                    known_info['embedding']
                )
                
                # Convert distance to confidence
                confidence = 1 / (1 + distance)
                
                if confidence >= confidence_threshold:
                    results.append((student_id, known_info['name'], confidence))
            
            # Sort by confidence (descending)
            results.sort(key=lambda x: x[2], reverse=True)
            return results
        
        except Exception as e:
            # Silently continue if no face detected in frame
            return []
    
    @staticmethod
    def _euclidean_distance(embedding1, embedding2):
        """Calculate Euclidean distance between two embeddings"""
        return np.sqrt(np.sum((np.array(embedding1) - np.array(embedding2)) ** 2))
    
    def set_distance_threshold(self, threshold):
        """Set the distance threshold for face matching"""
        self.distance_threshold = threshold
    
    def set_confidence_threshold(self, threshold):
        """Set the confidence threshold for face matching"""
        self.confidence_threshold = threshold
    
    def get_all_students(self):
        """Get all student names and IDs"""
        return [(sid, info['name']) for sid, info in self.known_embeddings.items()]


if __name__ == "__main__":
    # Test the recognizer
    from google_drive_downloader import GoogleDriveDownloader
    
    downloader = GoogleDriveDownloader("StudentPicsDataset.csv")
    photos_index = downloader.get_photos_index()
    
    recognizer = FaceRecognizer(photos_index)
    print(f"\n✅ Face recognizer ready with {len(recognizer.known_embeddings)} known faces")

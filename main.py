import cv2
import numpy as np
from google_drive_downloader import GoogleDriveDownloader
from face_recognizer import FaceRecognizer
import os
from pathlib import Path
from datetime import datetime
import json

class CameraFaceRecognition:
    """Real-time face recognition using webcam"""
    
    def __init__(self, csv_path="StudentPicsDataset.csv", confidence_threshold=0.6):
        """
        Initialize the camera-based face recognition system
        
        Args:
            csv_path: Path to CSV with student data
            confidence_threshold: Minimum confidence for a match
        """
        print("\n🚀 Initializing Face Recognition System...")
        
        # Download student photos
        self.downloader = GoogleDriveDownloader(csv_path)
        self.photos_index = self.downloader.get_photos_index()
        
        # Initialize face recognizer
        self.recognizer = FaceRecognizer(self.photos_index)
        self.confidence_threshold = confidence_threshold
        
        # Recognition history
        self.recognition_history = []
        self.recognition_log = "recognition_log.json"
        
        print(f"✅ System ready! Tracking {len(self.recognizer.known_embeddings)} students")
    
    def run_camera(self, window_width=1200, window_height=800, record_attendance=True):
        """
        Run real-time face recognition from webcam
        
        Args:
            window_width: Width of the display window
            window_height: Height of the display window
            record_attendance: Whether to log recognized faces
        """
        print("\n📷 Starting camera... Press 'Q' to quit, 'S' to save screenshot, 'R' to reset")
        print("=" * 70)
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Could not open camera")
            return
        
        # Set camera properties for better quality
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        recognized_students = {}  # Track recognized students in current session
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    print("❌ Error: Failed to read frame")
                    break
                
                frame_count += 1
                
                # Flip the frame for selfie view
                frame = cv2.flip(frame, 1)
                
                # Recognize faces in the frame
                results = self.recognizer.recognize_face_in_frame(
                    frame,
                    confidence_threshold=self.confidence_threshold
                )
                
                # Display results on frame
                frame = self._draw_results(frame, results)
                
                # Display information panel
                frame = self._draw_info_panel(frame, results, len(recognized_students))
                
                # Track recognized students
                if results:
                    best_match = results[0]
                    student_id = best_match[0]
                    student_name = best_match[1]
                    confidence = best_match[2]
                    
                    if student_id not in recognized_students:
                        recognized_students[student_id] = {
                            'name': student_name,
                            'confidence': confidence,
                            'first_seen': datetime.now().isoformat(),
                            'count': 0
                        }
                    recognized_students[student_id]['count'] += 1
                    
                    if record_attendance:
                        self._log_recognition(student_id, student_name, confidence)
                
                # Display the frame
                cv2.imshow('Student Face Recognition System', frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q'):
                    break
                elif key == ord('s') or key == ord('S'):
                    self._save_screenshot(frame, results)
                elif key == ord('r') or key == ord('R'):
                    recognized_students = {}
                    print("\n🔄 Recognition history cleared")
        
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted by user")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            
            # Display summary
            self._display_summary(recognized_students)
    
    def _draw_results(self, frame, results):
        """Draw recognition results on the frame"""
        h, w, _ = frame.shape
        
        if not results:
            # No face detected
            cv2.putText(frame, "No face detected", (50, h - 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
        else:
            # Draw top result
            best_match = results[0]
            student_name = best_match[1]
            confidence = best_match[2]
            
            # Draw a rectangle and text
            text = f"{student_name[:30]}"
            conf_text = f"Confidence: {confidence:.2%}"
            
            # Background for text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.2
            thickness = 2
            
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            conf_size = cv2.getTextSize(conf_text, font, font_scale - 0.3, thickness - 1)[0]
            
            # Draw colored rectangle
            color = (0, 255, 0) if confidence > 0.75 else (0, 165, 255) if confidence > 0.6 else (0, 0, 255)
            
            y_pos = h - 100
            cv2.rectangle(frame, (30, y_pos - 10), (30 + max(text_size[0], conf_size[0]) + 20, y_pos + 80),
                         color, -1)
            
            # Draw text
            cv2.putText(frame, text, (50, y_pos + 20),
                       font, font_scale, (255, 255, 255), thickness)
            cv2.putText(frame, conf_text, (50, y_pos + 55),
                       font, font_scale - 0.3, (255, 255, 255), thickness - 1)
            
            # Show alternative matches
            if len(results) > 1:
                y_alt = 50
                cv2.putText(frame, "Other matches:", (10, y_alt),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 100, 100), 1)
                for i, (sid, name, conf) in enumerate(results[1:4], 1):
                    y_alt += 30
                    alt_text = f"{i}. {name[:25]} ({conf:.1%})"
                    cv2.putText(frame, alt_text, (20, y_alt),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        
        return frame
    
    def _draw_info_panel(self, frame, results, recognized_count):
        """Draw information panel"""
        h, w, _ = frame.shape
        
        # Draw header
        cv2.rectangle(frame, (0, 0), (w, 60), (30, 30, 30), -1)
        cv2.putText(frame, "STUDENT FACE RECOGNITION SYSTEM", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Draw stats
        cv2.putText(frame, f"Recognized Today: {recognized_count}",
                   (w - 300, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1)
        
        # Draw footer instructions
        footer_y = h - 10
        cv2.putText(frame, "Q: Quit | S: Screenshot | R: Reset | Conf.Threshold: 0.6",
                   (10, footer_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
        
        return frame
    
    def _save_screenshot(self, frame, results):
        """Save a screenshot with recognition results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        
        filename = screenshots_dir / f"recognition_{timestamp}.jpg"
        cv2.imwrite(str(filename), frame)
        
        if results:
            best_match = results[0]
            print(f"📸 Screenshot saved: {filename}")
            print(f"   Recognized: {best_match[1]} (Confidence: {best_match[2]:.2%})")
        else:
            print(f"📸 Screenshot saved: {filename} (No face detected)")
    
    def _log_recognition(self, student_id, student_name, confidence):
        """Log a recognition event"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'student_id': str(student_id),
            'student_name': student_name,
            'confidence': float(confidence)
        }
        self.recognition_history.append(log_entry)
    
    def _display_summary(self, recognized_students):
        """Display summary of recognized students"""
        print("\n" + "=" * 70)
        print("📊 RECOGNITION SESSION SUMMARY")
        print("=" * 70)
        
        if not recognized_students:
            print("No students recognized in this session")
        else:
            print(f"\nTotal unique students recognized: {len(recognized_students)}\n")
            
            # Sort by detection count
            sorted_students = sorted(
                recognized_students.items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )
            
            print(f"{'ID':<12} {'Name':<30} {'Detections':<12} {'Avg Confidence':<15}")
            print("-" * 70)
            
            for student_id, info in sorted_students:
                print(f"{student_id:<12} {info['name'][:28]:<30} {info['count']:<12} {info['confidence']:.2%:<15}")
        
        # Save to JSON log
        if self.recognition_history:
            with open(self.recognition_log, 'a') as f:
                for entry in self.recognition_history:
                    json.dump(entry, f)
                    f.write('\n')
            print(f"\n✅ Recognition log saved to {self.recognition_log}")
        
        print("=" * 70)


if __name__ == "__main__":
    import sys
    
    csv_path = "StudentPicsDataset.csv"
    
    # Check if CSV exists
    if not Path(csv_path).exists():
        print(f"❌ Error: {csv_path} not found!")
        sys.exit(1)
    
    # Initialize and run
    system = CameraFaceRecognition(csv_path, confidence_threshold=0.6)
    system.run_camera(record_attendance=True)

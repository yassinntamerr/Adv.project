import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from threading import Thread
import json
from datetime import datetime
from google_drive_downloader import GoogleDriveDownloader
from face_recognizer import FaceRecognizer
import cv2
from PIL import Image, ImageTk
import numpy as np

class FaceRecognitionGUI:
    """GUI for Face Recognition System"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Student Face Recognition System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2b2b2b")
        
        # Initialize variables
        self.system = None
        self.camera_running = False
        self.cap = None
        self.photo_image = None
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the GUI interface"""
        
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(
            title_frame,
            text="🎓 Student Face Recognition System",
            font=("Arial", 18, "bold")
        )
        title_label.pack()
        
        # Status Frame
        status_frame = ttk.LabelFrame(self.root, text="System Status", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = ttk.Label(
            status_frame,
            text="🔴 System Not Initialized",
            font=("Arial", 11)
        )
        self.status_label.pack(side=tk.LEFT)
        
        self.stats_label = ttk.Label(
            status_frame,
            text="Students: 0 | Photos Downloaded: 0 | Recognized: 0",
            font=("Arial", 10)
        )
        self.stats_label.pack(side=tk.RIGHT)
        
        # Control Frame
        control_frame = ttk.LabelFrame(self.root, text="Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        self.init_button = ttk.Button(
            button_frame,
            text="Initialize System",
            command=self.initialize_system
        )
        self.init_button.pack(side=tk.LEFT, padx=5)
        
        self.camera_button = ttk.Button(
            button_frame,
            text="Start Camera",
            command=self.toggle_camera,
            state=tk.DISABLED
        )
        self.camera_button.pack(side=tk.LEFT, padx=5)
        
        self.screenshot_button = ttk.Button(
            button_frame,
            text="Take Screenshot (S)",
            command=self.take_screenshot,
            state=tk.DISABLED
        )
        self.screenshot_button.pack(side=tk.LEFT, padx=5)
        
        self.analyze_button = ttk.Button(
            button_frame,
            text="View Statistics",
            command=self.show_statistics,
            state=tk.DISABLED
        )
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = ttk.Button(
            button_frame,
            text="Quit",
            command=self.quit_app
        )
        self.quit_button.pack(side=tk.RIGHT, padx=5)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Settings", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(settings_frame, text="Confidence Threshold:").pack(side=tk.LEFT, padx=5)
        
        self.confidence_var = tk.DoubleVar(value=0.6)
        confidence_scale = ttk.Scale(
            settings_frame,
            from_=0.3,
            to=0.9,
            orient=tk.HORIZONTAL,
            variable=self.confidence_var,
            length=200
        )
        confidence_scale.pack(side=tk.LEFT, padx=5)
        
        self.confidence_label = ttk.Label(
            settings_frame,
            text="0.60",
            font=("Arial", 10)
        )
        self.confidence_label.pack(side=tk.LEFT, padx=5)
        
        confidence_scale.config(command=self.update_confidence)
        
        # Video Frame
        video_frame = ttk.LabelFrame(self.root, text="Camera Feed", padding=5)
        video_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.video_label = tk.Label(video_frame, bg="black")
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # Results Frame
        results_frame = ttk.LabelFrame(self.root, text="Last Recognition", padding=10)
        results_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.results_label = ttk.Label(
            results_frame,
            text="No recognition yet",
            font=("Arial", 11),
            foreground="gray"
        )
        self.results_label.pack(fill=tk.X)
    
    def initialize_system(self):
        """Initialize the face recognition system"""
        csv_path = Path("StudentPicsDataset.csv")
        
        if not csv_path.exists():
            messagebox.showerror("Error", "StudentPicsDataset.csv not found!")
            return
        
        self.status_label.config(text="🟡 Initializing system...")
        self.root.update()
        
        def init_thread():
            try:
                # Download photos
                downloader = GoogleDriveDownloader(str(csv_path))
                photos_index = downloader.download_all_photos()
                
                # Create recognizer
                self.system = FaceRecognizer(photos_index)
                
                # Update UI
                self.status_label.config(text="🟢 System Ready")
                self.camera_button.config(state=tk.NORMAL)
                self.analyze_button.config(state=tk.NORMAL)
                
                stats = f"Students: {len(self.system.known_embeddings)} | Photos Downloaded: {len(photos_index)} | Recognized: 0"
                self.stats_label.config(text=stats)
                
                messagebox.showinfo("Success", "System initialized successfully!")
            
            except Exception as e:
                self.status_label.config(text="🔴 Error During Initialization")
                messagebox.showerror("Error", f"Failed to initialize: {str(e)[:100]}")
        
        thread = Thread(target=init_thread, daemon=True)
        thread.start()
    
    def toggle_camera(self):
        """Toggle camera on/off"""
        if self.camera_running:
            self.stop_camera()
        else:
            self.start_camera()
    
    def start_camera(self):
        """Start camera feed"""
        if not self.system:
            messagebox.showwarning("Warning", "Initialize system first!")
            return
        
        self.camera_running = True
        self.camera_button.config(text="Stop Camera")
        self.screenshot_button.config(state=tk.NORMAL)
        self.cap = cv2.VideoCapture(0)
        
        def camera_loop():
            while self.camera_running and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                
                # Recognize faces
                results = self.system.recognize_face_in_frame(
                    frame,
                    confidence_threshold=self.confidence_var.get()
                )
                
                # Draw results
                h, w, _ = frame.shape
                
                if results:
                    best = results[0]
                    text = f"{best[1]}"
                    conf = f"{best[2]:.1%}"
                    
                    # Update last recognition label
                    self.results_label.config(
                        text=f"✅ {best[1]} (Confidence: {best[2]:.2%})",
                        foreground="green"
                    )
                    
                    # Draw on frame
                    cv2.putText(frame, text, (50, h - 60),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
                    cv2.putText(frame, conf, (50, h - 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    self.results_label.config(
                        text="⚠️ No face detected",
                        foreground="gray"
                    )
                
                # Convert to PhotoImage
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(rgb_frame)
                pil_image = pil_image.resize((self.video_label.winfo_width() or 640, 
                                             self.video_label.winfo_height() or 480))
                self.photo_image = ImageTk.PhotoImage(pil_image)
                
                self.video_label.config(image=self.photo_image)
                self.root.after(30)  # ~30 FPS
        
        thread = Thread(target=camera_loop, daemon=True)
        thread.start()
    
    def stop_camera(self):
        """Stop camera feed"""
        self.camera_running = False
        if self.cap:
            self.cap.release()
        self.camera_button.config(text="Start Camera")
        self.screenshot_button.config(state=tk.DISABLED)
        self.video_label.config(image='')
        self.photo_image = None
    
    def take_screenshot(self):
        """Take a screenshot"""
        if not self.camera_running:
            messagebox.showwarning("Warning", "Camera is not running!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        
        # Get the current frame
        ret, frame = self.cap.read()
        if ret:
            filename = screenshots_dir / f"screenshot_{timestamp}.jpg"
            cv2.imwrite(str(filename), frame)
            messagebox.showinfo("Success", f"Screenshot saved: {filename}")
    
    def show_statistics(self):
        """Show recognition statistics"""
        log_path = Path("recognition_log.json")
        
        if not log_path.exists():
            messagebox.showinfo("Info", "No recognition log yet.")
            return
        
        try:
            stats = {}
            with open(log_path, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    student_id = entry['student_id']
                    if student_id not in stats:
                        stats[student_id] = {
                            'name': entry['student_name'],
                            'count': 0,
                            'avg_confidence': 0,
                            'total_confidence': 0
                        }
                    stats[student_id]['count'] += 1
                    stats[student_id]['total_confidence'] += entry['confidence']
            
            # Calculate averages
            for sid in stats:
                if stats[sid]['count'] > 0:
                    stats[sid]['avg_confidence'] = stats[sid]['total_confidence'] / stats[sid]['count']
            
            # Create message
            message = "📊 Recognition Statistics\n\n"
            sorted_stats = sorted(stats.items(), key=lambda x: x[1]['count'], reverse=True)
            
            for sid, info in sorted_stats[:20]:  # Top 20
                message += f"{info['name']}: {info['count']} times (Avg: {info['avg_confidence']:.1%})\n"
            
            messagebox.showinfo("Statistics", message)
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not read log: {str(e)}")
    
    def update_confidence(self, value):
        """Update confidence threshold display"""
        conf_val = float(value)
        self.confidence_label.config(text=f"{conf_val:.2f}")
    
    def quit_app(self):
        """Quit the application"""
        self.stop_camera()
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionGUI(root)
    root.mainloop()

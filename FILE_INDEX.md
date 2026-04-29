# 📚 File Index & Documentation

## 🚀 Getting Started

### First Time Setup
1. **Read**: [QUICKSTART.md](QUICKSTART.md) - 5-minute quick start
2. **Run**: `python setup.py` - Install dependencies
3. **Test**: `python test_system.py` - Verify installation
4. **Run**: `python main.py` - Start recognition

### Recommended Reading Order
1. [QUICKSTART.md](QUICKSTART.md) - Overview & quick start
2. [README.md](README.md) - Comprehensive documentation
3. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technical details
4. [config.json](config.json) - Configuration options

---

## 📂 Files Explained

### Core Application Files

#### **main.py** - Command-line Interface
- **Purpose**: Real-time face recognition with webcam
- **Usage**: `python main.py`
- **Features**: 
  - Live camera feed
  - Real-time face recognition
  - Attendance logging
  - Screenshot capture
- **Controls**: Q (quit), S (screenshot), R (reset)

#### **gui_app.py** - Graphical User Interface
- **Purpose**: User-friendly GUI application
- **Usage**: `python gui_app.py`
- **Features**:
  - Graphical buttons and controls
  - Confidence threshold slider
  - Live video display
  - Statistics viewer
- **Ideal for**: Users who prefer graphical interfaces

#### **google_drive_downloader.py** - Photo Download
- **Purpose**: Download student photos from Google Drive
- **Key Class**: `GoogleDriveDownloader`
- **Functions**:
  - `download_all_photos()` - Download all photos
  - `extract_file_id()` - Parse Google Drive URLs
  - `get_photos_index()` - Get cached photos
- **Usage**: Used internally by main app

#### **face_recognizer.py** - Recognition Engine
- **Purpose**: Face recognition using DeepFace
- **Key Class**: `FaceRecognizer`
- **Functions**:
  - `recognize_face_in_image()` - Recognize in image
  - `recognize_face_in_frame()` - Recognize in video frame
  - `set_confidence_threshold()` - Adjust sensitivity
- **Model**: VGGFace2 (pre-trained deep learning model)

---

### Setup & Testing Files

#### **setup.py** - Automatic Setup
- **Purpose**: Install dependencies and verify setup
- **Usage**: `python setup.py`
- **Installs**:
  - All packages from requirements.txt
  - DeepFace models
  - Supporting libraries
- **Checks**:
  - Python version
  - CSV file existence
  - Camera accessibility

#### **test_system.py** - Diagnostic Tool
- **Purpose**: Verify complete system setup
- **Usage**: `python test_system.py`
- **Tests**:
  - Python version & dependencies
  - CSV file validity
  - Camera access
  - Module imports
  - Directory creation
- **Output**: Pass/fail report

#### **requirements.txt** - Dependencies
- **Purpose**: List all Python packages needed
- **Contents**:
  - deepface - Face recognition
  - opencv-python - Computer vision
  - tensorflow/keras - Deep learning
  - numpy, pandas - Data processing
  - pillow - Image processing
  - matplotlib - Visualization
- **Installation**: `pip install -r requirements.txt`

---

### Utility & Analysis Files

#### **analyze_logs.py** - Log Analysis
- **Purpose**: Analyze recognition logs and generate reports
- **Usage**: `python analyze_logs.py`
- **Output**:
  - recognition_report.csv - Statistics
  - recognition_analysis.png - Charts
- **Statistics**:
  - Recognition counts per student
  - Average confidence scores
  - Time-based analysis

#### **utilities.py** - System Utilities
- **Purpose**: Helper tools for system management
- **Usage**: `python utilities.py`
- **Menu Options**:
  - Validate CSV
  - Download photos
  - Prepare embeddings
  - System information
  - Export student lists
  - Clean cache

#### **run_system.bat** - Windows Launcher
- **Purpose**: Easy one-click launch on Windows
- **Usage**: Double-click the file
- **Checks**:
  - Python installation
  - Dependencies
  - CSV file

#### **run_system.sh** - Linux/Mac Launcher
- **Purpose**: Easy one-click launch on Linux/Mac
- **Usage**: `bash run_system.sh`
- **Checks**: Same as batch file

---

### Configuration Files

#### **config.json** - Configuration Settings
- **Purpose**: Customize system behavior
- **Settings**:
  - Recognition threshold (0.3-0.9)
  - Face model selection
  - Camera settings
  - Display options
  - Performance options
  - Feature toggles

#### **StudentPicsDataset.csv** - Student Data (Your File)
- **Required**: Yes, must be in project folder
- **Format**: CSV with 3 columns:
  - Student ID
  - Student Name
  - Photo Link (Google Drive URLs)
- **Source**: You provided this file

---

### Documentation Files

#### **README.md** - Complete Documentation
- **Sections**:
  - Features overview
  - Installation instructions
  - How to use
  - Advanced configuration
  - Troubleshooting
  - Performance metrics
  - Module documentation
- **Length**: Comprehensive (~500+ lines)

#### **QUICKSTART.md** - Quick Start Guide
- **Sections**:
  - 5-minute setup
  - Command-line vs GUI
  - Expected behavior
  - Quick configuration
  - Q&A section
- **Length**: Quick reference (~200 lines)

#### **PROJECT_SUMMARY.md** - Technical Overview
- **Sections**:
  - Project overview
  - File structure
  - How it works (diagrams)
  - Module descriptions
  - Configuration options
  - Requirements
  - Performance benchmarks
  - Usage examples

#### **FILE_INDEX.md** - This File
- **Purpose**: Navigate all project files
- **Contains**: File descriptions and usage

---

### Runtime Directories (Auto-Created)

#### **student_photos/** - Downloaded Photos Cache
- **Auto-created**: Yes, on first run
- **Contents**: Downloaded student photos
- **Naming**: `{student_id}_{student_name}.jpg`
- **Purpose**: Local cache to avoid re-downloading

#### **screenshots/** - Saved Screenshots
- **Auto-created**: On first screenshot
- **Contents**: Captured recognition screenshots
- **Naming**: `screenshot_{timestamp}.jpg`
- **Purpose**: Record of recognized students

#### **recognition_log.json** - Recognition Log
- **Auto-created**: On first recognition
- **Format**: JSON, one entry per line
- **Contents**: 
  - Timestamp
  - Student ID
  - Student Name
  - Confidence score
- **Purpose**: Complete recognition history

---

## 🎯 Common Tasks & Which Files to Use

### Task: Install System
```bash
python setup.py
```
📄 Files: `setup.py`, `requirements.txt`

### Task: Run Face Recognition
```bash
python main.py              # Command-line
python gui_app.py           # With GUI
bash run_system.sh          # Linux/Mac
# or double-click run_system.bat (Windows)
```
📄 Files: `main.py`, `gui_app.py`, `google_drive_downloader.py`, `face_recognizer.py`

### Task: Test System
```bash
python test_system.py
```
📄 Files: `test_system.py`, all dependencies

### Task: Analyze Results
```bash
python analyze_logs.py
```
📄 Files: `analyze_logs.py`, `recognition_log.json`

### Task: Manage System
```bash
python utilities.py
```
📄 Files: `utilities.py`, `google_drive_downloader.py`, `face_recognizer.py`

### Task: Configure Settings
Edit `config.json` or `main.py` directly
📄 Files: `config.json`, `main.py`

### Task: View Documentation
- Quick start → [QUICKSTART.md](QUICKSTART.md)
- Full docs → [README.md](README.md)
- Technical → [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 🔑 Key Concepts

### Face Embeddings
A mathematical representation of a face extracted using deep learning. Two similar faces have similar embeddings (small distance).

### Confidence Score
A value from 0-1 indicating how confident the system is about a match:
- > 0.75 = High confidence (green)
- 0.6-0.75 = Medium confidence (orange)
- < 0.6 = Low confidence (red)

### Distance Metric
Euclidean distance between face embeddings. Lower distance = more similar faces.

### VGGFace2
A pre-trained deep learning model for face recognition. Very accurate and widely used.

---

## 📊 File Dependencies

```
main.py
  ├── google_drive_downloader.py
  │   └── requests, pandas
  ├── face_recognizer.py
  │   ├── deepface
  │   ├── opencv (cv2)
  │   └── numpy
  └── cv2, json, datetime

gui_app.py
  ├── tkinter (built-in)
  ├── google_drive_downloader.py
  ├── face_recognizer.py
  ├── cv2
  └── PIL

analyze_logs.py
  ├── json
  ├── pandas
  ├── matplotlib
  └── pathlib
```

---

## ✅ Pre-Execution Checklist

- [ ] Python 3.8+ installed
- [ ] `StudentPicsDataset.csv` in project folder
- [ ] `requirements.txt` in project folder
- [ ] Internet connection (for photo downloads)
- [ ] Webcam connected and working
- [ ] At least 2GB free disk space
- [ ] 4GB+ RAM available
- [ ] All Python files downloaded

---

## 🚨 Troubleshooting by File

### `setup.py` fails
- Check Python version: `python --version`
- Verify internet connection
- Check pip installation: `python -m pip --version`

### `main.py` fails
- Run `test_system.py` first for diagnostics
- Check `StudentPicsDataset.csv` exists
- Ensure camera is connected
- Try `python gui_app.py` instead

### `google_drive_downloader.py` fails
- Check internet connection
- Verify Google Drive links are accessible
- Check file ID extraction in code

### `face_recognizer.py` fails
- Verify photos downloaded: check `student_photos/` folder
- Check GPU/CPU resources
- Try lowering confidence threshold

### `analyze_logs.py` fails
- Ensure `recognition_log.json` exists
- Check matplotlib installation
- Verify pandas works: `python -c "import pandas"`

---

## 📖 Reading Guide by Role

### Student New to Face Recognition
1. [QUICKSTART.md](QUICKSTART.md)
2. [README.md](README.md) - Features section
3. Run: `python main.py`

### Advanced User / Tweaker
1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. [config.json](config.json)
3. Modify: `face_recognizer.py` and `main.py`

### Project Manager / Presenter
1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. [README.md](README.md) - Key Features
3. Run: `python analyze_logs.py` for demo

### Debugger / Troubleshooter
1. [README.md](README.md) - Troubleshooting
2. Run: `python test_system.py`
3. Check: Module imports and logs
4. Review: `google_drive_downloader.py`, `face_recognizer.py`

---

## 🔗 Quick Links

- **🚀 Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **📖 Full Docs**: [README.md](README.md)
- **🔧 Technical**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **⚙️ Config**: [config.json](config.json)
- **🎯 This Index**: [FILE_INDEX.md](FILE_INDEX.md)

---

**Last Updated**: April 2026
**Project Status**: ✅ Production Ready
**All Files**: 10 core Python files + 5 documentation files


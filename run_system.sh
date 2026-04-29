#!/bin/bash

# Face Recognition System - Command Line Interface
# This script starts the face recognition system on Linux/Mac

echo ""
echo "================================================"
echo "   STUDENT FACE RECOGNITION SYSTEM"
echo "   Advanced Statistics Project"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "[INFO] Python version: $PYTHON_VERSION"

# Check if requirements are installed
python3 -c "import deepface" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[WARNING] Dependencies not installed"
    echo "[INFO] Running setup..."
    python3 setup.py
    if [ $? -ne 0 ]; then
        echo "[ERROR] Setup failed"
        exit 1
    fi
fi

# Check if CSV exists
if [ ! -f "StudentPicsDataset.csv" ]; then
    echo "[ERROR] StudentPicsDataset.csv not found!"
    echo "[INFO] Please place the CSV file in this directory"
    exit 1
fi

# Run main application
echo ""
echo "[INFO] Starting Face Recognition System..."
echo "[INFO] Press Ctrl+C to stop"
echo ""

python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Application failed"
    exit 1
fi

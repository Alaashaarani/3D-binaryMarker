# Underwater Marker Detection and 3D Binary Marker STL Designs


## Repository Contents

### 1. Required libraries

OpenCV for python

### 2. Underwater Marker Detection (Aqualoc Detector)

The `detector.py` file contains the `aquaLocDetector` class which implements detection of modified ArUco markers designed for underwater environments.

Key Features:
- Supports multiple image processing methods:
  - CLAHE (Contrast Limited Adaptive Histogram Equalization)
  - Iterative thresholding
  - Normalization-based approach
- Customizable marker dictionary and IDs
- Performance timing metrics
- Visualization options for debugging

Basic Usage:
```python
detector = aquaLocDetector()
detector.enable_display()  # Optional: enable visualization
detector.set_method(0)     # Select processing method (0=CLAHE, 1=Iterative, 2=Normalization)

# For each frame:
corners, ids, rejected = detector.detect_aqualoc(image_frame)

# How to use the Design: 

From the 3D-BM_stl folder. 
1- Pick the ArUco marker, and print using white color (Available 4x4_DICT_ARUCO ID:13-14-15-28-30-34-35-41-42-43-49). 
2- Pick the Enclosure and print using black color: 
  a- No pattern, recommended as it is faster to print. 
  b- With pattern, only in very clear scenarios. 

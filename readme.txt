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
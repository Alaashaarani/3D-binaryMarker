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

# Code Basic Usage:
```python
detector = aquaLocDetector()
detector.enable_display()  # Optional: enable visualization
detector.set_method(0)     # Select processing method (0=CLAHE, 1=Iterative, 2=Normalization)

# For each frame:
corners, ids, rejected = detector.detect_aqualoc(image_frame)

```

# How to use the Design: 
From the 3D-BM_stl folder. 
1- Pick the ArUco marker, and print using white color (Available 4x4_DICT_ARUCO ID:13-14-15-28-30-34-35-41-42-43-49). 
2- Pick the Enclosure and print using black color: 
  a- No pattern, recommended as it is faster to print. 
  b- With pattern, only in very clear scenarios. 


# Bibtex Citation: 

@Article{jmse13081442,
AUTHOR = {Chaarani, Alaaeddine and Cieslak, Patryk and Esteba, Joan and Eichhardt, Ivan and Ridao, Pere},
TITLE = {Three-Dimensional Binary Marker: A Novel Underwater Marker Applicable for Long-Term Deployment Scenarios},
JOURNAL = {Journal of Marine Science and Engineering},
VOLUME = {13},
YEAR = {2025},
NUMBER = {8},
ARTICLE-NUMBER = {1442},
URL = {https://www.mdpi.com/2077-1312/13/8/1442},
ISSN = {2077-1312},
DOI = {10.3390/jmse13081442}
}




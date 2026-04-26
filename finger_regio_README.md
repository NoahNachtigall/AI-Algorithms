# Finger Region Detection

This Python script uses MediaPipe to detect and track hand and face landmarks in real-time using your webcam.

## Features
- Hand landmark detection with up to 2 hands
- Face landmark detection with blendshapes and transformation matrices
- Real-time video processing
- Frame count logging every 30 frames

## Requirements
- Python 3.x
- OpenCV (cv2)
- MediaPipe
- Required model files: `hand_landmarker.task` and `face_landmarker.task` (included in this directory)

## Installation
1. Install dependencies:
   ```
   pip install opencv-python mediapipe
   ```

## Usage
Run the script:
```
python finger_regio.py
```
- A window titled "Hand & Face Tracking" will open showing the camera feed with detected landmarks.
- Press ESC in the video window to exit.

## Notes
- Ensure your webcam is accessible.
- The script processes frames continuously; performance may vary based on hardware.
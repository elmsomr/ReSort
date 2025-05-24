# YOLOv11n Real-Time Inference with Pi Camera 3

This project provides a Python script to run real-time object detection using a YOLOv11n model with the Raspberry Pi Camera 3. It supports live video display with bounding boxes and optional recording of the output.

## Features

- Real-time object detection using YOLOv11n.
- Capture video from Raspberry Pi Camera 3.
- Display detected objects with bounding boxes and confidence scores.
- Optional recording of the inference video (`demo1.avi`).
- FPS and object count overlay on the display.

## Requirements

- Python 3.8+
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- OpenCV (`opencv-python`)
- numpy
- picamera2 (for Raspberry Pi Camera 3 support)

## Installation

```bash
pip install ultralytics opencv-python numpy
sudo apt-get install -y python3-picamera2
```

## Usage

```bash
python your.py --model runs/detect/train/weights/best.pt --resolution 640x480
```

Add --record flag to save the video output:

```bash
python your.py --model runs/detect/train/weights/best.pt --resolution 640x480 --record
```

## Controls

- Press `q` to quit.
- Press `s` to pause.
- Press `p` to save a snapshot (`capture.png`).

## Notes

- Ensure the model path is correct.
- The resolution must be specified as `WIDTHxHEIGHT` (e.g., `640x480`).
- Tested on Raspberry Pi OS with Pi Camera 3.


import os
import sys
import argparse
import time

import cv2
import numpy as np
from ultralytics import YOLO

# Parse command-line arguments
parser = argparse.ArgumentParser(description="YOLO Inference using Pi Camera 3")
parser.add_argument('--model', required=True, help='Path to YOLO model (e.g. "runs/detect/train/weights/best.pt")')
parser.add_argument('--resolution', required=True, help='Resolution for inference display and recording, format: WxH (e.g. "640x480")')
parser.add_argument('--record', action='store_true', help='Record output to demo1.avi')

args = parser.parse_args()

# Parse arguments
model_path = args.model
user_res = args.resolution
record = args.record

# Check model existence
if not os.path.exists(model_path):
    print("ERROR: Model path is invalid or model was not found.")
    sys.exit(1)

# Parse resolution
try:
    resW, resH = map(int, user_res.lower().split('x'))
except:
    print("ERROR: Invalid resolution format. Use format: WxH (e.g. 640x480)")
    sys.exit(1)

# Load YOLO model
model = YOLO(model_path, task='detect')
labels = model.names

# Initialize PiCamera2
from picamera2 import Picamera2
picam = Picamera2()
picam.configure(picam.create_video_configuration(main={"format": 'RGB888', "size": (resW, resH)}))
picam.start()

# Video recording setup
if record:
    record_fps = 30
    recorder = cv2.VideoWriter("demo1.avi", cv2.VideoWriter_fourcc(*'MJPG'), record_fps, (resW, resH))

# Define bounding box colors (Tableau 10)
bbox_colors = [(164,120,87), (68,148,228), (93,97,209), (178,182,133), (88,159,106), 
               (96,202,231), (159,124,168), (169,162,241), (98,118,150), (172,176,184)]

# Frame rate calculation variables
fps_buffer = []
fps_avg_len = 200
avg_fps = 0

# Inference loop
while True:
    t_start = time.perf_counter()

    # Capture frame
    frame = picam.capture_array()
    if frame is None:
        print("ERROR: Unable to capture from Pi Camera.")
        break

    # Run inference
    results = model(frame, verbose=False)
    detections = results[0].boxes
    object_count = 0

    # Draw detections
    for i in range(len(detections)):
        xyxy = detections[i].xyxy.cpu().numpy().squeeze().astype(int)
        xmin, ymin, xmax, ymax = xyxy
        class_id = int(detections[i].cls.item())
        confidence = detections[i].conf.item()
        label = labels[class_id]

        if confidence > 0.5:
            color = bbox_colors[class_id % len(bbox_colors)]
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
            label_text = f"{label}: {int(confidence * 100)}%"
            label_size, baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            label_y = max(ymin, label_size[1] + 10)
            cv2.rectangle(frame, (xmin, label_y - label_size[1] - 10), 
                          (xmin + label_size[0], label_y + baseline - 10), color, cv2.FILLED)
            cv2.putText(frame, label_text, (xmin, label_y - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            object_count += 1

    # Calculate FPS
    t_end = time.perf_counter()
    fps = 1 / (t_end - t_start)
    if len(fps_buffer) >= fps_avg_len:
        fps_buffer.pop(0)
    fps_buffer.append(fps)
    avg_fps = np.mean(fps_buffer)

    # Overlay info
    cv2.putText(frame, f"FPS: {avg_fps:.2f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame, f"Objects: {object_count}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Show result
    cv2.imshow("ReSort", frame)
    if record:
        recorder.write(frame)

    # Handle keypress
    key = cv2.waitKey(5)
    if key in [ord('q'), ord('Q')]:
        break
    elif key in [ord('s'), ord('S')]:
        cv2.waitKey()
    elif key in [ord('p'), ord('P')]:
        cv2.imwrite("capture.png", frame)

# Cleanup
print(f"Average FPS: {avg_fps:.2f}")
picam.stop()
if record:
    recorder.release()
cv2.destroyAllWindows()

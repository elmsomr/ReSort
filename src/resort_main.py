import os
import sys
import argparse
import glob
import time
import requests
import json
from datetime import datetime
import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from gpiozero import OutputDevice, DigitalInputDevice
import RPi.GPIO as GPIO
import math

# Optional API config
API_URL = "http://...:5000/api/waste"
API_HEADERS = {"Content-Type": "application/json"}
ENABLE_API = False

# Motor pin configurations
STEPPER1_PINS = {'dir': 20, 'step': 21, 'enable': 16}  # Conveyor
STEPPER2_PINS = {'dir': 19, 'step': 26, 'enable': 13}  # Lateral shift
LIMIT_SWITCH_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup stepper motor pins
for pin in list(STEPPER1_PINS.values()) + list(STEPPER2_PINS.values()):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Setup limit switch
GPIO.setup(LIMIT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Stepper control functions
def move_stepper(pins, steps, direction, delay=0.00015):
    GPIO.output(pins['dir'], GPIO.HIGH if direction == 'right' else GPIO.LOW)
    GPIO.output(pins['enable'], GPIO.LOW)
    for _ in range(steps):
        GPIO.output(pins['step'], GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(pins['step'], GPIO.LOW)
        time.sleep(delay)
    GPIO.output(pins['enable'], GPIO.HIGH)

def calibrate_to_origin():
    print("[INFO] Homing in progress...")

    GPIO.output(STEPPER2_PINS['dir'], GPIO.LOW)  # go left
    GPIO.output(STEPPER2_PINS['enable'], GPIO.LOW)

    step_delay = 0.0002  # 200 µs for microstepping

    while GPIO.input(LIMIT_SWITCH_PIN):
        t0 = time.perf_counter()
        GPIO.output(STEPPER2_PINS['step'], GPIO.HIGH)
        while time.perf_counter() - t0 < step_delay:
            pass

        t1 = time.perf_counter()
        GPIO.output(STEPPER2_PINS['step'], GPIO.LOW)
        while time.perf_counter() - t1 < step_delay:
            pass

    GPIO.output(STEPPER2_PINS['enable'], GPIO.HIGH)

    # After reaching limit switch return to the center (16500 step right)
    move_stepper(STEPPER2_PINS, 16500, 'right')

    print("[INFO] Center position reached.")

# API payload sender
def send_to_api(payload):
    if ENABLE_API:
        try:
            filtered_payload = {k: payload[k] for k in ['track_id', 'global_id', 'class', 'timestamp']}
            response = requests.post(API_URL, json=filtered_payload, headers=API_HEADERS)
            print(f"[API] Sent payload: {filtered_payload} - Status: {response.status_code}")
        except Exception as e:
            print(f"[API Error] {e}")

# Track global ID
def get_last_global_id(log_path="log.jsonl"):
    if not os.path.exists(log_path):
        return 1
    last_id = 0
    with open(log_path, "r") as f:
        for line in f:
            try:
                obj = json.loads(line.strip())
                last_id = max(last_id, int(obj.get("global_id", 0)))
            except:
                continue
    return last_id + 1

# Waste class to position map (motor steps from center)
waste_positions = {
    'paper': 850,
    'metal': 13000,
    'plastic': 22000,
    'glass': 34000
}

# Argparse
parser = argparse.ArgumentParser()
parser.add_argument('--model', required=True)
parser.add_argument('--source', required=True)
parser.add_argument('--thresh', default=0.5, type=float)
parser.add_argument('--resolution', default=None)
parser.add_argument('--record', action='store_true')
args = parser.parse_args()

model_path = args.model
img_source = args.source
min_thresh = args.thresh
user_res = args.resolution
record = args.record

model = YOLO(model_path, task='detect')
labels = model.names

resize = False
if user_res:
    resize = True
    resW, resH = map(int, user_res.split('x'))

if os.path.isdir(img_source):
    source_type = 'folder'
elif os.path.isfile(img_source):
    ext = os.path.splitext(img_source)[1].lower()
    source_type = 'image' if ext in ['.jpg', '.jpeg', '.png', '.bmp'] else 'video' if ext in ['.avi', '.mov', '.mp4', '.mkv', '.wmv'] else sys.exit(0)
elif img_source.startswith('usb'):
    source_type = 'usb'
    usb_idx = int(img_source[3:])
elif img_source.startswith('picamera'):
    source_type = 'picamera'
else:
    print('Invalid input source.')
    sys.exit(0)

if source_type == 'image':
    imgs_list = [img_source]
elif source_type == 'folder':
    imgs_list = [f for f in glob.glob(img_source + '/*') if os.path.splitext(f)[1].lower() in ['.jpg', '.jpeg', '.png', '.bmp']]
elif source_type == 'video':
    cap = cv2.VideoCapture(img_source)
elif source_type == 'usb':
    cap = cv2.VideoCapture(usb_idx)
elif source_type == 'picamera':
    from picamera2 import Picamera2
    cap = Picamera2()
    if resize:
        cap.configure(cap.create_video_configuration(main={"format": 'RGB888', "size": (resW, resH)}))
    else:
        cap.configure(cap.create_video_configuration(main={"format": 'RGB888'}))
    cap.start()

if record:
    if source_type not in ['video', 'usb'] or not user_res:
        print('Recording only for video/cam and resolution required.')
        sys.exit(0)
    recorder = cv2.VideoWriter('recorded.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (resW, resH))

tracker = DeepSort(max_age=10, n_init=3, max_cosine_distance=0.4)
sent_ids = set()
global_id_counter = get_last_global_id()
track_to_global = {}
fps_buffer = []
fps_buffer_len = 200
img_count = 0

# Information variables
last_detected_class = "None"
last_detected_id = "-"
target_position = "-"
movement_direction = "-"
movement_steps = 0
conveyor_active = False
returning = False

calibrate_to_origin()

while True:
    t_start = time.time()

    if source_type in ['image', 'folder']:
        if img_count >= len(imgs_list): break
        frame = cv2.imread(imgs_list[img_count])
        img_count += 1
    elif source_type in ['video', 'usb']:
        ret, frame = cap.read()
        if not ret: break
    elif source_type == 'picamera':
        frame = cap.capture_array()
        if frame is None: break

    if resize:
        frame = cv2.resize(frame, (resW, resH))

    results = model(frame, verbose=False)
    detections = results[0].boxes
    det_for_tracking = []

    for i in range(len(detections)):
        conf = detections[i].conf.item()
        if conf < min_thresh: continue
        xyxy = detections[i].xyxy.cpu().numpy().squeeze().astype(int)
        classidx = int(detections[i].cls.item())
        classname = labels[classidx]
        det_for_tracking.append(([xyxy[0], xyxy[1], xyxy[2], xyxy[3]], conf, classname))

    tracks = tracker.update_tracks(det_for_tracking, frame=frame)

    for track in tracks:
        if not track.is_confirmed(): continue
        track_id = track.track_id
        if track_id in sent_ids: continue
        sent_ids.add(track_id)

        if track_id not in track_to_global:
            track_to_global[track_id] = global_id_counter
            global_id_counter += 1

        global_id = track_to_global[track_id]
        l, t, r, b = map(int, track.to_ltrb())
        classname = track.get_det_class()
        conf = track.get_det_conf()

        payload = {
            "track_id": track_id,
            "global_id": global_id,
            "class": classname,
            "conf": round(conf, 2),
            "timestamp": datetime.now().isoformat()
        }

        send_to_api(payload)

        # Update last informations
        last_detected_class = classname
        last_detected_id = global_id
        target_position = waste_positions.get(classname, 16000)
        movement_direction = 'right' if target_position > 16000 else 'left'
        movement_steps = abs(target_position - 16000)

        # Move lateral motor
        move_stepper(STEPPER2_PINS, movement_steps, movement_direction)
        time.sleep(0.5)

        # Activate conveyor motor
        conveyor_active = True
        move_stepper(STEPPER1_PINS, 2400, 'left')  # 3 round
        conveyor_active = False
        time.sleep(0.5)

        # Return lateral motor back to origin
        returning = True
        calibrate_to_origin()
        returning = False

        # Draw box
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(frame, f"{classname} [{global_id}]", (l, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Calculate FPS 
    t_end = time.time()
    fps = 1 / (t_end - t_start + 1e-5)
    fps_buffer.append(fps)
    if len(fps_buffer) > fps_buffer_len:
        fps_buffer.pop(0)
    avg_fps = sum(fps_buffer) / len(fps_buffer)

    # Information display drawing
    info_lines = [
        f"FPS: {avg_fps:.2f}",
        f"Last Detected: {last_detected_class}",
        f"Track ID: {last_detected_id}",
        f"Target Position: {target_position}",
        f"Moving Lateral Motor: {movement_direction.upper()} ({movement_steps} steps)",
        "Conveyor: ACTIVE" if conveyor_active else "Conveyor: IDLE",
        "Status: Returning to center..." if returning else "Status: Ready"
    ]

    y0, dy = 30, 25
    for i, line in enumerate(info_lines):
        y = y0 + i * dy
        cv2.putText(frame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow("ReSort", frame)
    if record:
        recorder.write(frame)

    key = cv2.waitKey(0 if source_type in ['image', 'folder'] else 5)
    if key == ord('q'): break

if source_type in ['video', 'usb']: cap.release()
elif source_type == 'picamera': cap.stop()
if record: recorder.release()
cv2.destroyAllWindows()

if fps_buffer:
    print(f"\nAverage FPS: {sum(fps_buffer) / len(fps_buffer):.2f}")

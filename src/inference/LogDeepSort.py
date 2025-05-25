import os
import sys
import argparse
import glob
import time
import json
from datetime import datetime
import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Optional API config (disabled by default)
api_url = "http://localhost:5000/api"  # Update when ready
headers = {"Content-Type": "application/json"}
ENABLE_API = False  # Change to True when API becomes active

def send_to_api(payload):
    if ENABLE_API:
        try:
            response = requests.post(api_url, json=payload, headers=headers)
            print(f"[API] Sent ID {payload['global_id']} - Status: {response.status_code}")
        except Exception as e:
            print(f"[API Error] {e}")

# Load last global_id from log file
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

model = YOLO(model_path)
labels = model.names

img_ext = ['.jpg', '.jpeg', '.png', '.bmp']
vid_ext = ['.avi', '.mov', '.mp4', '.mkv', '.wmv']

if os.path.isdir(img_source):
    source_type = 'folder'
elif os.path.isfile(img_source):
    ext = os.path.splitext(img_source)[1].lower()
    source_type = 'image' if ext in img_ext else 'video' if ext in vid_ext else sys.exit(0)
elif 'usb' in img_source:
    source_type = 'usb'
    usb_idx = int(img_source[3:])
elif 'picamera' in img_source:
    source_type = 'picamera'
    picam_idx = int(img_source[8:])
else:
    print('Invalid input source.')
    sys.exit(0)

resize = False
if user_res:
    resize = True
    resW, resH = map(int, user_res.split('x'))

if record:
    if source_type not in ['video', 'usb'] or not user_res:
        print('Recording only for video/cam and resolution required.')
        sys.exit(0)
    recorder = cv2.VideoWriter('recorded.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (resW, resH))

if source_type == 'image':
    imgs_list = [img_source]
elif source_type == 'folder':
    imgs_list = [f for f in glob.glob(img_source + '/*') if os.path.splitext(f)[1].lower() in img_ext]
elif source_type in ['video', 'usb']:
    cap = cv2.VideoCapture(img_source if source_type == 'video' else usb_idx)
    if resize:
        cap.set(3, resW)
        cap.set(4, resH)
elif source_type == 'picamera':
    from picamera2 import Picamera2
    cap = Picamera2()
    cap.configure(cap.create_video_configuration(main={"format": 'RGB888', "size": (resW, resH)}))
    cap.start()

tracker = DeepSort(max_age=10, n_init=3, max_cosine_distance=0.4)
sent_ids = set()
log_file_path = "log.jsonl"
log_file = open(log_file_path, "a")

# Global ID counter (persistent)
global_id_counter = get_last_global_id(log_file_path)
track_to_global = {}

# FPS tracking with buffer
fps_buffer = []
fps_buffer_len = 200

img_count = 0
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

        # Map to global ID
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

        # Log
        log_file.write(json.dumps(payload) + "\n")
        log_file.flush()
        print(f"[LOG] {payload}")

        # Send to API (optional)
        send_to_api(payload)

        # Draw
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(frame, f"{classname} [{global_id}]", (l, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # FPS hesapla ve ekrana yazdır (filtrelenmiş)
    t_end = time.time()
    fps = 1 / (t_end - t_start + 1e-5)
    fps_buffer.append(fps)
    if len(fps_buffer) > fps_buffer_len:
        fps_buffer.pop(0)
    avg_fps = sum(fps_buffer) / len(fps_buffer)
    cv2.putText(frame, f"FPS: {avg_fps:.2f}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Detection", frame)
    if record:
        recorder.write(frame)

    key = cv2.waitKey(0 if source_type in ['image', 'folder'] else 5)
    if key == ord('q'): break

if source_type in ['video', 'usb']: cap.release()
elif source_type == 'picamera': cap.stop()
if record: recorder.release()
cv2.destroyAllWindows()
log_file.close()

# Ortalama FPS yazdır
if fps_buffer:
    final_avg_fps = sum(fps_buffer) / len(fps_buffer)
    print(f"\nOrtalama FPS: {final_avg_fps:.2f}")

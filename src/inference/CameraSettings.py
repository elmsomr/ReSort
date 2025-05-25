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
    if not user_res:
        print("Picamera için --resolution gereklidir. Örn: --resolution 640x480")
        sys.exit(0)
    cap.configure(cap.create_video_configuration(main={"format": 'RGB888', "size": (resW, resH)}))
    cap.start()

    lens_position = 5.0
    brightness = 0.0
    contrast = 1.0
    zoom_factor=1.0
    
    cap.set_controls({
        "AfMode": 0,
        "LensPosition": lens_position,
        "Brightness": brightness,
        "Contrast": contrast
    })

tracker = DeepSort(max_age=10, n_init=3, max_cosine_distance=0.4)
sent_ids = set()
log_file_path = "log.jsonl"
log_file = open(log_file_path, "a")

global_id_counter = get_last_global_id(log_file_path)
track_to_global = {}

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
        if zoom_factor != 1.0:
            h, w = frame.shape[:2]
            new_w = int(w / zoom_factor)
            new_h = int(h / zoom_factor)
            x1 = (w - new_w) // 2
            y1 = (h - new_h) // 2
            cropped = frame[y1:y1+new_h, x1:x1+new_w]
            frame = cv2.resize(cropped, (w, h))
        


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

        log_file.write(json.dumps(payload) + "\n")
        log_file.flush()
        print(f"[LOG] {payload}")

        send_to_api(payload)
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(frame, f"{classname} [{global_id}]", (l, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    t_end = time.time()
    fps = 1 / (t_end - t_start + 1e-5)
    fps_buffer.append(fps)
    if len(fps_buffer) > fps_buffer_len:
        fps_buffer.pop(0)
    avg_fps = sum(fps_buffer) / len(fps_buffer)

    cv2.putText(frame, f"FPS: {avg_fps:.2f}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    if source_type == 'picamera':
        cv2.putText(frame, f"LensPos: {lens_position:.1f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, f"Brightness: {brightness:.1f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, f"Contrast: {contrast:.1f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv2.imshow("Detection", frame)
    if record:
        recorder.write(frame)

    key = cv2.waitKey(0 if source_type in ['image', 'folder'] else 5) 
    if key == ord('q'): break
    elif key == ord('+') or key == ord('='):
        zoom_factor = min(zoom_factor + 0.1, 2.0)
        print(f"Zoom artırıldı: {zoom_factor:.1f}x")
    elif key == ord('-') or key == ord('_'):
        zoom_factor = max(zoom_factor - 0.1, 1.0)
        print(f"Zoom azaltıldı: {zoom_factor:.1f}x")


    if source_type == 'picamera':
        if key == ord('w'):
            lens_position = min(lens_position + 0.1, 10.0)
            cap.set_controls({"LensPosition": lens_position})
        elif key == ord('e'):
            lens_position = max(lens_position - 0.1, 0.0)
            cap.set_controls({"LensPosition": lens_position})
        elif key == ord('a'):
            cap.set_controls({"AfMode": 2})
        elif key == ord('m'):
            cap.set_controls({"AfMode": 0, "LensPosition": lens_position})
        elif key == ord('s'):
            brightness = max(brightness - 0.1, -1.0)
            cap.set_controls({"Brightness": brightness})
        elif key == ord('d'):
            brightness = min(brightness + 0.1, 1.0)
            cap.set_controls({"Brightness": brightness})
        elif key == ord('z'):
            contrast = min(contrast + 0.5, 16.0)
            cap.set_controls({"Contrast": contrast})
        elif key == ord('x'):
            contrast = max(contrast - 0.5, 0.0)
            cap.set_controls({"Contrast": contrast})

if source_type in ['video', 'usb']: cap.release()
elif source_type == 'picamera': cap.stop()
if record: recorder.release()
cv2.destroyAllWindows()
log_file.close()

if fps_buffer:
    final_avg_fps = sum(fps_buffer) / len(fps_buffer)
    print(f"\nOrtalama FPS: {final_avg_fps:.2f}")

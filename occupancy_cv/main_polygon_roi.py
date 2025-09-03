import cv2
from ultralytics import YOLO
import numpy as np
import json

# File path 
video_path = "occupancy_cv/test.mp4"
output_path = "output_with_polygons.mp4"
desk_rois_path = "occupancy_cv/desk_roi_pos.json"

# Save data into a json file
with open("data.json", "w") as f:
    json.dump({}, f)
    
# Step 2a: Load JSON file
with open(desk_rois_path, "r") as f:
    desk_rois_json = json.load(f)

# Dict of the rois pos
DESK_ROIS = {desk: np.array(roi, dtype=np.int32) for desk, roi in desk_rois_json.items()}

# Define YOLO model
model = YOLO("yolov8l.pt")
print(model.names)

# Setup cv2
cap = cv2.VideoCapture(video_path)
frame_index = 0

# Errro handling for file open error
if not cap.isOpened():
    print(f"Error: Could not open file {video_path}")
    exit()
    
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Smoothing memory
desk_last_seen = {seat: -999 for seat in DESK_ROIS}
SMOOTH_FRAMES = fps * 10

# Detection internal
DETECTION_INTERVAL = fps * 1

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

all_status = {}

# Main loop for each frame detection
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    desk_status = {desk_name: 'Vacant' for desk_name in DESK_ROIS}
    
    results = []
    if frame_index % DETECTION_INTERVAL == 0:
        results = model(frame, conf=0.1)
    
    if results:
        for result in results:
            boxes = result.boxes
            for box in boxes:
                if model.names[int(box.cls)] == 'person':
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    person_center_point = ((x1 + x2) // 2, (y1 + y2) // 2)
                    
                    for desk_name, polygon in DESK_ROIS.items():
                        is_inside = cv2.pointPolygonTest(polygon, person_center_point, False)
                        
                        if is_inside >= 0:
                            desk_status[desk_name] = 'Occupied'
                            desk_last_seen[desk_name] = frame_index 
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            break
    for desk_name in DESK_ROIS:
        if frame_index - desk_last_seen[desk_name] <= SMOOTH_FRAMES:
            desk_status[desk_name] = "Occupied"
                
    for desk_name, polygon in DESK_ROIS.items():
        status = desk_status[desk_name]
        color = (0, 255, 0) if status == 'Vacant' else (0, 0, 255)
    
        cv2.polylines(frame, [polygon], isClosed=True, color=color, thickness=2)
    
        text_pos = (polygon[0][0], polygon[0][1])
        cv2.putText(frame, f'{desk_name}: {status}', text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    

    all_status[frame_index] = desk_status.copy()

            
    out.write(frame)
    cv2.imshow('Desk Occupancy Detection', frame)
    
    frame_index += 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

with open("log.json", "w") as f:
    json.dump(all_status, f, indent=4)
print("Log file saved as log.json")

cap.release()
out.release()
cv2.destroyAllWindows()
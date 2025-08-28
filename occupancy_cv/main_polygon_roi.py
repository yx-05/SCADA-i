import cv2
from ultralytics import YOLO
import numpy as np

model = YOLO("yolo11m.pt")
print(model.names)

video_path = "seatoccupancytest.mp4"
output_path = "output_with_polygons.mp4"

DESK_ROIS = {
    'Desk 1': np.array([
        [179,214], [1,299], [46,359], [163,359], [271,275]
    ], np.int32),
    'Desk 2': np.array([
        [96,131], [131,158], [157,219], [5,279], [3,153]
    ], np.int32),
    'Desk 3': np.array([
        [100,128], [182,109], [208,132], [229,184], [150,198], [129,159], [101,132]
    ], np.int32),
    'Desk 4': np.array([
        [181,197], [273,163], [371,196], [274,262]
    ], np.int32),
    'Desk 5': np.array([
        [371,110], [442,128], [479,99], [410,77]
    ], np.int32)
}

# Smoothing memory
desk_last_seen = {seat: -999 for seat in DESK_ROIS}
SMOOTH_FRAMES = 5

cap = cv2.VideoCapture(video_path)
frame_index = 0

if not cap.isOpened():
    print(f"Error: Could not open file {video_path}")
    exit()
    
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    desk_status = {desk_name: 'Vacant' for desk_name in DESK_ROIS}
    
    results = model(frame, conf=0.1)
    
    for result in results:
        boxes = result.boxes
        # detected = False
        for box in boxes:
            if model.names[int(box.cls)] == 'person':
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                person_center_point = ((x1 + x2) // 2, (y1 + y2) // 2)
                
                for desk_name, polygon in DESK_ROIS.items():
                    is_inside = cv2.pointPolygonTest(polygon, person_center_point, False)
                    
                    if is_inside >= 0:
                        # detected = True
                        desk_status[desk_name] = 'Occupied'
                        desk_last_seen[desk_name] = frame_index 
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        break
                    else:
                        if frame_index - desk_last_seen[desk_name] <= SMOOTH_FRAMES:
                            desk_status[desk_name] = "Occupied"
               
        for desk_name, polygon in DESK_ROIS.items():
            status = desk_status[desk_name]
            color = (0, 255, 0) if status == 'Vacant' else (0, 0, 255)
        
            cv2.polylines(frame, [polygon], isClosed=True, color=color, thickness=2)
        
            text_pos = (polygon[0][0], polygon[0][1] - 10)
            cv2.putText(frame, f'{desk_name}: {status}', text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
    out.write(frame)
    cv2.imshow('Desk Occupancy Detection', frame)
    
    frame_index += 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
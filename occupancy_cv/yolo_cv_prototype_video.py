# occupancy_detector.py

import cv2
from ultralytics import YOLO
import numpy as np
import json
import os

# ---- CONFIG ----
VIDEO_PATH = "occupancy_cv/test_video_2.mp4"
OUTPUT_VIDEO_PATH = "output_occupancy_video.mp4"
DESK_ROIS_PATH = "occupancy_cv/roi_pos.json"
LOG_FILE_PATH = "occupancy_log.json"

# Frame resolution must match the annotation script
FIXED_WIDTH = 1280
FIXED_HEIGHT = 720
# ---------------

# Step 1: Load ROI data from JSON file
if not os.path.exists(DESK_ROIS_PATH):
    print(f"Error: ROI file not found at '{DESK_ROIS_PATH}'")
    print("Please run the 'roi_annotator.py' script first to generate it.")
    exit()

with open(DESK_ROIS_PATH, "r") as f:
    desk_rois_json = json.load(f)

# Convert ROI lists to NumPy arrays for OpenCV
DESK_ROIS = {desk: np.array(roi, dtype=np.int32) for desk, roi in desk_rois_json.items()}

# Step 2: Initialize YOLO model
try:
    model = YOLO("yolov8l.pt")
except Exception as e:
    print(f"Error initializing YOLO model: {e}")
    print("Please ensure you have an internet connection for the first run to download the model.")
    exit()

# Step 3: Setup video capture and writer
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print(f"Error: Could not open video file at '{VIDEO_PATH}'")
    exit()

fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, fps, (FIXED_WIDTH, FIXED_HEIGHT))

# Step 4: Initialize tracking variables
frame_index = 0
all_status_logs = {}

print("\n--- OCCUPANCY DETECTOR ---")
print(f"Processing video: {VIDEO_PATH}")
print(f"Loaded {len(DESK_ROIS)} desk ROIs.")
print("Press [q] to stop the process early.")
print("--------------------------\n")

# Main processing loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Processing finished.")
        break

    # !! CRITICAL FOR SYNCHRONIZATION !!
    # Resize frame to the same dimensions used during annotation
    frame = cv2.resize(frame, (FIXED_WIDTH, FIXED_HEIGHT))

    # Initialize status for all desks in the current frame
    desk_status = {desk_name: 'Vacant' for desk_name in DESK_ROIS}

    # Run YOLO detection on the frame
    results = model(frame, classes=[0], conf=0.4, verbose=False) # class 0 is 'person'

    # Process detection results
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            # Calculate the center of the bottom edge of the box (feet position)
            person_anchor_point = ((x1 + x2) // 2, (y1 + y2) // 2)

            # Check if this person's anchor point is inside any desk polygon
            for desk_name, polygon in DESK_ROIS.items():
                is_inside = cv2.pointPolygonTest(polygon, person_anchor_point, False)
                if is_inside >= 0:
                    desk_status[desk_name] = 'Occupied'
                    # Optional: draw the person's bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                    break # Person can only occupy one desk at a time

    # Draw polygons and status text on the frame
    for desk_name, polygon in DESK_ROIS.items():
        status = desk_status[desk_name]
        color = (0, 255, 0) if status == 'Vacant' else (0, 0, 255) # Green for Vacant, Red for Occupied

        # Draw the polygon ROI
        cv2.polylines(frame, [polygon], isClosed=True, color=color, thickness=2)

        # Calculate text position (e.g., top-left corner of the polygon)
        text_pos = (polygon[0][0], polygon[0][1] - 10)
        cv2.putText(frame, f'{desk_name}: {status}', text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Log the status for the current frame
    all_status_logs[frame_index] = desk_status.copy()

    # Write the processed frame to the output video
    out.write(frame)

    # Display the frame
    cv2.imshow('Desk Occupancy Detection', frame)

    frame_index += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Processing stopped by user.")
        break

# Save the log file
with open(LOG_FILE_PATH, "w") as f:
    json.dump(all_status_logs, f, indent=4)
print(f"\n💾 Occupancy log file saved to {LOG_FILE_PATH}")
print(f"💾 Processed video saved to {OUTPUT_VIDEO_PATH}")

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
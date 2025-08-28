from ultralytics import YOLO
import cv2

# --- CONFIGURATION ---
model = YOLO('yolo11x.pt') 

video_path = 'seatoccupancytest.mp4'
output_path = "output_with_rois.mp4"

# ==============================================================================
# === NEW: DEFINE YOUR DESK REGIONS OF INTEREST (ROIs) HERE ===
# You MUST replace these coordinates with the actual coordinates from your video.
# Format: 'Desk Name': (x1, y1, x2, y2)
DESK_ROIS = {
    'Desk 1': (2, 207, 266, 358),
    'Desk 2': (103, 110, 231, 195),
    'Desk 3': (228, 88, 320, 159),
    'Desk 4': (343, 115, 429, 228),
}
# ==============================================================================

# --- VIDEO SETUP ---
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error: Could not open video file {video_path}")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

print("Processing video with ROI checks...")

# --- MAIN PROCESSING LOOP ---
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # ==============================================================================
    # === NEW: Initialize the status for each desk for the current frame ===
    desk_status = {desk_name: 'Vacant' for desk_name in DESK_ROIS}
    # ==============================================================================

    # Run YOLOv8 inference on the frame
    results = model(frame)

    # Process the detection results
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Check if the detected object is a 'person'
            if model.names[int(box.cls)] == 'person':
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # --- NEW: Check if the center of the person is inside any ROI ---
                # Calculate the center of the detected person's box
                person_center_x = (x1 + x2) // 2
                person_center_y = (y1 + y2) // 2

                for desk_name, (dx1, dy1, dx2, dy2) in DESK_ROIS.items():
                    if dx1 < person_center_x < dx2 and dy1 < person_center_y < dy2:
                        desk_status[desk_name] = 'Occupied'
                        # Optional: Draw the person's box only if they occupy a desk
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        break # Person is assigned to a desk, no need to check other desks

    # ==============================================================================
    # === NEW: Draw the ROI boxes and their status on the frame ===
    for desk_name, (dx1, dy1, dx2, dy2) in DESK_ROIS.items():
        status = desk_status[desk_name]
        color = (0, 255, 0) if status == 'Vacant' else (0, 0, 255) # Green if vacant, Red if occupied
        
        # Draw the ROI rectangle
        cv2.rectangle(frame, (dx1, dy1), (dx2, dy2), color, 2)
        
        # Put the status text
        cv2.putText(frame, f'{desk_name}: {status}', (dx1, dy1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    # ==============================================================================

    # Write the frame with all drawings to the output video
    out.write(frame)

    # Optional: Display a real-time preview
    cv2.imshow('Desk Occupancy Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- CLEANUP ---
print("Processing finished.")
cap.release()
out.release()
cv2.destroyAllWindows()
print(f"Output video with ROIs saved to: {output_path}")
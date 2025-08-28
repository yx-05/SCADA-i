from ultralytics import YOLO
import cv2

# --- CONFIGURATION ---
# Load a pre-trained YOLOv8 model
# <-- FIX 1: Corrected model name from 'yolo11n.pt' to 'yolov8n.pt'
model = YOLO('yolo11m.pt')  

# Path to the video you want to label
video_path = 'seatoccupancytest.mp4'
output_path = "outputvid.mp4"

# --- VIDEO SETUP ---
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error: Could not open video file {video_path}")
    exit()

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# <-- FIX 2: Used the 'output_path' variable for the output file
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# print("Processing video... Press 'q' in the preview window to stop early.")
frame_count = 0

# --- MAIN PROCESSING LOOP ---
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 inference on the frame
    results = model(frame)

    # Process the results
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Check if the detected object is a 'person'
            if model.names[int(box.cls)] == 'person':
                # Get bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Draw the bounding box (Green color)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Create the label text (class name + confidence)
                confidence = box.conf[0]
                label = f'Person: {confidence:.2f}'
                
                # Put the label on the image (White text on a green background)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Write the frame with detections to the output video
    out.write(frame)

    # # <-- IMPROVEMENT: Add a real-time preview window
    # cv2.imshow('YOLOv8 Real-Time Detection', frame)
    
    # # Allow early exit by pressing 'q'
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    
    # # <-- IMPROVEMENT: Print progress
    # frame_count += 1
    # if frame_count % 20 == 0: # Print progress every 20 frames
    #     print(f"Processed {frame_count} frames...")


# --- CLEANUP ---
print("Processing finished.")
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Output video saved successfully to: {output_path}")
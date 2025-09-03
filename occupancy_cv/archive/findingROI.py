# Python script to locate the position of each seat in a frame for a fix vid

import cv2
import json

vid_path = "occupancy_cv/test.mp4"

cap = cv2.VideoCapture(vid_path)

# Dict to save labeled points
seat_pos = {}

# Current seat being label
current_seat = ""
points = []

def click_event(event, x, y, flags, param):
    global points, frame_copy
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])
        # Annotate small circle to visualize the point
        cv2.circle(frame_copy, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Frame", frame_copy)
        print(f"Pixel pos: x:{x}, y:{y}")

count = 1       
current_seat = f"Desk {count}"
        
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_event)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_copy = frame.copy()
    # Draw previously added points
    for pt in points:
        cv2.circle(frame_copy, tuple(pt), 5, (0, 0, 255), -1)
    
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(30) & 0xFF
    
    if key == ord('p'):   # Press 'p' to pause (freeze)
        while True:
            cv2.imshow("Frame", frame)   # show the same frame
            key2 = cv2.waitKey(0) & 0xFF # wait indefinitely
            if key2 == ord('c'):         # Press 'c' to continue
                break
            
    elif key == 13:  # Enter key to save current seat points
        if points:
            seat_pos[current_seat] = points
            print(f"Saved points for {current_seat}:", points)
            count += 1
            current_seat = f"Desk {count}"
            points = []
        else:
            print("No points to save!")
    
    elif key == ord('q'):  # Quit
        break

print('yo')
if seat_pos:
    with open("roi_pos.json", "w") as f:
        json.dump(seat_pos, f, indent=4)
    print("All points saved to roi_pos.json")

cap.release()
cv2.destroyAllWindows()
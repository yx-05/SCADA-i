import cv2
import json

# ---- CONFIG ----
vid_path = "occupancy_cv/test_video_2.mp4"
OUTPUT_JSON = "roi_pos.json"
FIXED_WIDTH = 1280
FIXED_HEIGHT = 720
# ---------------

cap = cv2.VideoCapture(vid_path)

seat_pos = {}
points = []
count = 1
current_seat = f"Desk {count}"
paused = False

def click_event(event, x, y, flags, param):
    global points, frame_copy
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])
        cv2.circle(frame_copy, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Frame", frame_copy)
        print(f"Pixel pos: x:{x}, y:{y}")

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_event)

while cap.isOpened():
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break

        # ✅ FORCE FIXED SIZE EVERY FRAME
        frame = cv2.resize(frame, (FIXED_WIDTH, FIXED_HEIGHT))
        frame_copy = frame.copy()

    # redraw clicked points
    for pt in points:
        cv2.circle(frame_copy, tuple(pt), 5, (0, 0, 255), -1)

    cv2.imshow("Frame", frame_copy)
    key = cv2.waitKey(30) & 0xFF

    if key == ord('p'):  # pause
        paused = not paused
        print("⏸ Paused" if paused else "▶ Resumed")

    elif key == 13:  # ENTER = save ROI polygon
        if points:
            seat_pos[current_seat] = points.copy()
            print(f"✅ Saved {current_seat}: {points}")
            count += 1
            current_seat = f"Desk {count}"
            points = []
            frame_copy = frame.copy()
        else:
            print("⚠ No points to save!")

    elif key == ord('c'):  # continue if paused
        paused = False
        print("▶ Resumed")

    elif key == ord('q'):  # quit
        break

# Save ROI JSON
if seat_pos:
    with open(OUTPUT_JSON, "w") as f:
        json.dump(seat_pos, f, indent=4)
    print(f"💾 Saved all ROI points to {OUTPUT_JSON}")

cap.release()
cv2.destroyAllWindows()

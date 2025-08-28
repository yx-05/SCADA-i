import cv2

cap = cv2.VideoCapture("seatoccupancytest.mp4")

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Pixel pos: x:{x}, y:{y}")
        
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_event)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(30) & 0xFF
    
    if key == ord('p'):   # Press 'p' to pause (freeze)
        while True:
            cv2.imshow("Frame", frame)   # show the same frame
            key2 = cv2.waitKey(0) & 0xFF # wait indefinitely
            if key2 == ord('c'):         # Press 'c' to continue
                break
    
    elif key == ord('q'):  # Quit
        break

cap.release()
cv2.destroyAllWindows()
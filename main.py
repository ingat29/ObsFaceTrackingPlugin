import cv2

# 1. Connect to the webcam (0 is usually the default built-in or USB camera)
cap = cv2.VideoCapture(0)

print("Opening webcam... Press 'q' to quit.")

# 2. Create an infinite loop to read the video feed frame-by-frame
while True:
    # 'ret' is a boolean (True/False) checking if the frame was grabbed
    # 'frame' is the actual image data from the camera
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    # 3. Show the frame in a window
    cv2.imshow('Hamster Tracker Vision', frame)
    
    # 4. Wait 1 millisecond for a key press. If that key is 'q', break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 5. Clean up: Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
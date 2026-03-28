import cv2
import mediapipe as mp

#mediapipe hand tracker initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Connect to webcam (0 is default camera)
cap = cv2.VideoCapture(0)

print("Opening webcam... Press 'q' to quit.")

while True:
    # 'ret' is a boolean checking if the frame was grabbed
    # 'frame' is the actual image data
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

    result_hands = hands.process(rgb_frame)  # process the frame to find hands

    if result_hands.multi_hand_landmarks:  # if hands are detected
        for hand_landmarks in result_hands.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS) 

    result_face = face_mesh.process(rgb_frame) # process the frame to find faces

    if result_face.multi_face_landmarks:
        for face_landmarks in result_face.multi_face_landmarks:
            mp_draw.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

    cv2.imshow('Face tracker vision', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): # & 0xFF is used to get the last 8 bits of the key code, because the rest bits could be affected by using numlock or other keyboard settings. ord('q') is the ASCII code for 'q'.
        break

cap.release()
cv2.destroyAllWindows()
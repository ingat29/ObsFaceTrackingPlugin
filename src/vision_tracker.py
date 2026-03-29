import cv2
import mediapipe as mp

class VisionTracker:
    def __init__(self):
        
        # Mediapipe initialization for hand and face tracking
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        
        self.mp_draw = mp.solutions.drawing_utils
        
        # Connect to webcam (0 is default camera)
        self.cap = cv2.VideoCapture(0)

    def process_frame(self):
        # 'ret' is a boolean checking if the frame was grabbed
        # 'frame' is the actual image data
        ret, frame = self.cap.read()
        
        if not ret:
            return False, None, None, None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result_hands = self.hands.process(rgb_frame)
        result_face = self.face_mesh.process(rgb_frame)

        if result_hands.multi_hand_landmarks:
            for hand_landmarks in result_hands.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS) 

        if result_face.multi_face_landmarks:
            for face_landmarks in result_face.multi_face_landmarks:
                self.mp_draw.draw_landmarks(frame, face_landmarks, self.mp_face_mesh.FACEMESH_TESSELATION)

        return True, frame, result_hands, result_face

    def close(self):
        self.cap.release()
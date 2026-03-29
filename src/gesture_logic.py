import math

class GestureLogic:
    def __init__(self):
        self.MOUTH_OPEN_THRESHOLD = 0.20
        self.SMILE_THRESHOLD = 0.65

    def calculate_distance(self, point1, point2):
        return math.hypot(point2.x - point1.x, point2.y - point1.y)
    
    def calculate_distance_normalized(self, point1, point2, face_landmarks):
        # face_height = self.calculate_distance(face_landmarks[10], face_landmarks[152])
        # if face_height == 0:
        #     return 0
#^^^^^^^^ OLD NORMALIZATION -- i found face height normalization is not very stable

        interocular_distance = self.calculate_distance(face_landmarks[33], face_landmarks[263])
        # print(f"Interocular distance: {interocular_distance}")

        if interocular_distance == 0:
            return 0
        
        distance = self.calculate_distance(point1, point2)

        # ratio = distance / face_height
        ratio = distance / interocular_distance

        return ratio


    def detect_expression(self, face_data):
        
        if not face_data or not face_data.multi_face_landmarks:
            return "NEUTRAL"

        face_landmarks = face_data.multi_face_landmarks[0].landmark

        # 1. Check for Mouth Open
        # mouth_height = self.calculate_distance(face_landmarks[13], face_landmarks[14])
        mouth_height_normalized = self.calculate_distance_normalized(face_landmarks[13], face_landmarks[14], face_landmarks)
        
        # 2. Check for Smile (Mouth Width)
        # mouth_width = self.calculate_distance(face_landmarks[61], face_landmarks[291])
        mouth_width_normalized = self.calculate_distance_normalized(face_landmarks[61], face_landmarks[291], face_landmarks)

        # print(f"Mouth height (normalized): {mouth_height_normalized:.4f}, Mouth width (normalized): {mouth_width_normalized:.4f}")

        if mouth_height_normalized > self.MOUTH_OPEN_THRESHOLD:
            return "MOUTH_OPEN"
        elif mouth_width_normalized > self.SMILE_THRESHOLD:
            return "SMILE"
        else:
            return "NEUTRAL"
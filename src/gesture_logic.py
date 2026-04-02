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

    def detect_hand_gesture(self, hand_data):
        if not hand_data or not hand_data.multi_hand_landmarks:
            return None

        hand = hand_data.multi_hand_landmarks[0].landmark

            # # Verify if the thumb is up 
            # thumb_is_up = hand[4].y < hand[3].y and hand[4].y < hand[2].y # hand[3] and hand[2] are joint trackers

            # # Verify if the other four fingers are folded into a fist 
            # # (Comparing the fingertip Y to the knuckle Y)
            # index_folded = hand[8].y > hand[6].y
            # middle_folded = hand[12].y > hand[10].y
            # ring_folded = hand[16].y > hand[14].y
            # pinky_folded = hand[20].y > hand[18].y
            # ^^^^^^^^^^^^^^^^^ Prone to false positives, because sometimes the hand can be tilted, and the Y coordinate may not be a good indicator of whether the finger is folded or not

        # Helper function: distance from the wrist (Point 0) to any given point
        def dist_to_wrist(point_index):
            return self.calculate_distance(hand[0], hand[point_index])

        # Verify the thumb is extended? 
        # (Tip [4] is further from the wrist than the middle joint [3])
        thumb_extended = dist_to_wrist(4) > dist_to_wrist(3)

        # Verify that the fingers are folded into a fist? 
        # (Tips [8, 12, 16, 20] are closer to the wrist than the middle knuckles [6, 10, 14, 18])
        index_folded = dist_to_wrist(8) < dist_to_wrist(6)
        middle_folded = dist_to_wrist(12) < dist_to_wrist(10)
        ring_folded = dist_to_wrist(16) < dist_to_wrist(14)
        pinky_folded = dist_to_wrist(20) < dist_to_wrist(18)

        # If all conditions are met, it's a thumbs up!
        if thumb_extended and index_folded and middle_folded and ring_folded and pinky_folded:
            return "THUMBS_UP"
            
        return "HAND_TRACKED_BUT_NO_GESTURE"
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
        landmarks = hand_data.multi_hand_landmarks
        FINGERTIPS_THRESHOLD = 0.08
        WRIST_THRESHOLD = 0.15
        if not hand_data or not landmarks:
            return None

        #TWO-HAND GESTURE DETECTION

        if len(landmarks) == 2:
            hand1 = landmarks[0].landmark
            hand2 = landmarks[1].landmark
            
            # 1. Check if fingertips are touching 
            thumb_dist = self.calculate_distance(hand1[4], hand2[4])
            index_dist = self.calculate_distance(hand1[8], hand2[8])
            middle_dist = self.calculate_distance(hand1[12], hand2[12])
            ring_dist = self.calculate_distance(hand1[16], hand2[16])
            pinky_dist = self.calculate_distance(hand1[20], hand2[20])
            
            # 2. Check if wrists are far apart (forming the triangle base)
            wrist_dist = self.calculate_distance(hand1[0], hand2[0])

            # print(f"Thumb tip distance: {thumb_dist:.4f}, Index tip distance: {index_dist:.4f}, Middle tip distance: {middle_dist:.4f}, Ring tip distance: {ring_dist:.4f}, Pinky tip distance: {pinky_dist:.4f}, Wrist distance: {wrist_dist:.4f}")
            
            # If tips are close (< 0.08) AND wrists are separated (> 0.15)
            if (thumb_dist < FINGERTIPS_THRESHOLD and index_dist < FINGERTIPS_THRESHOLD and 
                middle_dist < FINGERTIPS_THRESHOLD and ring_dist < FINGERTIPS_THRESHOLD and pinky_dist < FINGERTIPS_THRESHOLD and wrist_dist > WRIST_THRESHOLD):
                return "STEEPLE"

        #SINGLE HAND GESTURE DETECTION

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

        is_thumb_gesture = thumb_extended and index_folded and middle_folded and ring_folded and pinky_folded

        if is_thumb_gesture:  
            if hand[4].y < hand[0].y: 
                return "THUMBS_UP"  
            else:
                return "THUMBS_DOWN"          
        return "HAND_TRACKED_BUT_NO_GESTURE"
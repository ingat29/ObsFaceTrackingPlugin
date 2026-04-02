import cv2
from gesture_logic import GestureLogic
from vision_tracker import VisionTracker
from obs_controller import OBSController

def main():
    print("Initializing Vision Engine...")
    tracker = VisionTracker()
    logic = GestureLogic()
    obs_link = OBSController(password="password123")

    print("Engine running. Press 'q' to quit.")
    
    current_state = "NEUTRAL"

    while True:
        success, frame, hand_data, face_data = tracker.process_frame()
        
        if not success:
            print("Failed to grab frame. Exiting...")
            break
        
        hand_gesture = logic.detect_hand_gesture(hand_data)

        face_expression = logic.detect_expression(face_data)
        
        # State machine - priority to hand gestures, then face expressions
        final_state = "NEUTRAL"
        if hand_gesture == "THUMBS_UP":
            final_state = "THUMBS_UP"
        else:
            final_state =face_expression

        if final_state != current_state:
            print(f"State changed to: {final_state}")
            obs_link.change_avatar(final_state) # Send to obs
            current_state = final_state

        cv2.imshow('Hamster Tracker Vision', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):   # & 0xFF is used to get the last 8 bits of the key code, because the rest bits could be affected by using numlock or other keyboard settings. ord('q') is the ASCII code for 'q'.
            break

    tracker.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
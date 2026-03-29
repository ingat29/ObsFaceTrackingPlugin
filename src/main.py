import cv2
from gesture_logic import GestureLogic
from vision_tracker import VisionTracker

def main():
    print("Initializing Vision Engine...")
    tracker = VisionTracker()
    logic = GestureLogic()
    
    print("Engine running. Press 'q' to quit.")
    
    current_expression = "NEUTRAL"

    while True:
        success, frame, hand_data, face_data = tracker.process_frame()
        
        if not success:
            print("Failed to grab frame. Exiting...")
            break
            
        new_expression = logic.detect_expression(face_data)
        if new_expression != current_expression:
            print(f"Expression detected: {new_expression}")
            current_expression = new_expression

        cv2.imshow('Hamster Tracker Vision', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):   # & 0xFF is used to get the last 8 bits of the key code, because the rest bits could be affected by using numlock or other keyboard settings. ord('q') is the ASCII code for 'q'.
            break

    tracker.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
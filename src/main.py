import cv2
from vision_tracker import VisionTracker

def main():
    print("Initializing Vision Engine...")
    tracker = VisionTracker()
    
    print("Engine running. Press 'q' to quit.")
    
    while True:
        success, frame, hand_data, face_data = tracker.process_frame()
        
        if not success:
            print("Failed to grab frame. Exiting...")
            break
            
        cv2.imshow('Hamster Tracker Vision', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):   # & 0xFF is used to get the last 8 bits of the key code, because the rest bits could be affected by using numlock or other keyboard settings. ord('q') is the ASCII code for 'q'.
            break

    tracker.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
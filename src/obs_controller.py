import os
import obsws_python as obs

class OBSController:
    def __init__(self, host='localhost', port=4455, password='password123'): # remember to replace this with template 
        print("Connecting to OBS WebSocket...")
        try:
            self.client = obs.ReqClient(host=host, port=port, password=password)
            print("Successfully connected to OBS!")
        except Exception as e:
            print(f"FAILED to connect to OBS. Is it running? Error: {e}")
            self.client = None

        # The exact name of the Image Source in your OBS scene
        self.source_name = "Hamster_Avatar"
        
        # We need absolute file paths for OBS to read the images correctly
        # This dynamically finds the 'assets' folder no matter where the script is run
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets_dir = os.path.join(base_dir, 'assets')
        
        # Make sure these filenames exactly match the images in the assets folder
        self.image_paths = {
            "NEUTRAL": os.path.join(assets_dir, "Neutral.png"),
            "SMILE": os.path.join(assets_dir, "Smile.png"),
            "MOUTH_OPEN": os.path.join(assets_dir, "Mouth Open.png"),
            "THUMBS_UP": os.path.join(assets_dir, "Thumbs Up.png"),
            # Fallback for when tracking hands but no gesture is made
            "HAND_TRACKED_BUT_NO_GESTURE": os.path.join(assets_dir, "Neutral.png") 
        }

    def change_avatar(self, expression):
        if not self.client:
            return # Skip if OBS isn't connected
            
        if expression not in self.image_paths:
            return # Skip if we don't have an image for this expression

        new_image_path = self.image_paths[expression]
        
        try:
            # This is the specific OBS v5 command to change a source's settings
            self.client.set_input_settings(
                self.source_name, 
                {"file": new_image_path}, 
                True
            )
        except Exception as e:
            print(f"Error sending command to OBS: {e}")
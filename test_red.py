from vilib import Vilib
import time

def main():
    print("Starting camera feed...")
    # Initialize the camera
    Vilib.camera_start(vflip=False, hflip=False)
    # Start the web stream so you can see what the car sees
    Vilib.display(local=False, web=True)
    time.sleep(2) # Give the camera sensor time to warm up
    
    print("\n" + "="*50)
    print("🚦 STOP SIGN TESTER 🚦")
    print("Open your browser to: http://<YOUR_PI_IP>:9000/mjpg")
    print("Press Ctrl+C to exit.")
    print("="*50 + "\n")
    
    # Enable red color detection to look for the stop sign
    Vilib.color_detect("red")
    
    try:
        while True:
            # Check how many red objects are currently detected
            num_red_objects = Vilib.detect_obj_parameter.get('color_n', 0)
            
            if num_red_objects != 0:
                # Get the dimensions and coordinates of the largest red object
                width = Vilib.detect_obj_parameter.get('color_w', 0)
                height = Vilib.detect_obj_parameter.get('color_h', 0)
                x = Vilib.detect_obj_parameter.get('color_x', 0)
                y = Vilib.detect_obj_parameter.get('color_y', 0)
                
                # Print the raw data to help you tune your threshold
                print(f"🔴 Red Object -> Width: {width} | Height: {height} | Center: ({x}, {y})")
                
                # Test against our Step 9 threshold (width > 40)
                if width > 40:
                    print("   🛑 TRIGGER: This is large enough to be considered a Stop Sign!")
            else:
                # Overwrite the same line to keep the terminal clean when nothing is seen
                print("Looking for red objects...", end='\r', flush=True)
                
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\nExiting test...")
    finally:
        # Cleanly release the camera resources
        Vilib.camera_close()

if __name__ == "__main__":
    main()
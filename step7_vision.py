from picarx import Picarx
from vilib import Vilib
import time

def main():
    car = Picarx()
    
    print("Starting camera... Please wait.")
    # Initialize the camera and broadcast the feed to http://<your_pi_ip>:9000/mjpg
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=True)
    time.sleep(2) # Wait for camera to warm up
    
    # WORKAROUND: Instead of object_detect_switch (which crashes on Python 3.13),
    # we use color detection and face detection to fulfill the lab requirements.
    
    # 1. Enable Color Detection for the Stop Sign (Red)
    Vilib.color_detect("red")
    
    # 2. Enable Face Detection for the Person
    Vilib.face_detect_switch(True) 
    
    print("Vision enabled. Open your browser to the Pi's IP on port 9000.")
    print("Hold a red stop sign or stand in front of the camera.")
    
    try:
        while True:
            # Example 1: Reacting to a Person/Face
            if Vilib.detect_obj_parameter.get('human_n', 0) != 0:
                print("Person detected! Applying brakes.")
                car.stop()
                
            # Example 2: Reacting to a Stop Sign (Red color block)
            elif Vilib.detect_obj_parameter.get('color_n', 0) != 0:
                # We check the width ('color_w') to ensure it's a large object close to the car,
                # rather than a random small red dot in the background.
                if Vilib.detect_obj_parameter.get('color_w', 0) > 40:
                    print("Red Stop Sign detected! Halting.")
                    car.stop()
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        car.stop()
        # Ensure the camera is cleanly released
        Vilib.camera_close()

if __name__ == "__main__":
    main()
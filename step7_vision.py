from picarx import Picarx
from vilib import Vilib
import time

def main():
    car = Picarx()
    
    print("Starting camera...")
    # Initialize the camera and send the feed to http://ip:9000/mjpg
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=True)
    time.sleep(2) # buffer to wait for camera to warm up
    
    # Due to Python version (our OS does not support some version), we use color_detect 
    # not object_detect_switch
    
    # 1. Enable Color Detection for the Stop Sign (Red)
    Vilib.color_detect("red")
    
    # 2. Enable Face Detection for the Person
    Vilib.face_detect_switch(True) 
    
    print("Vision enabled")
    
    try:
        while True:
            # 1. Reacting to a Person/Face
            if Vilib.detect_obj_parameter.get('human_n', 0) != 0:
                print("Person detected! Applying brakes.")
                car.stop()
                
            # 2: Reacting to a Stop Sign (Red color block)
            elif Vilib.detect_obj_parameter.get('color_n', 0) != 0:
                # We check the width (color_w) to ensure it's a large object close to the car,
                # rather than a random small red dot in the background.
                if Vilib.detect_obj_parameter.get('color_w', 0) > 40:
                    print("Red Stop Sign detected! Halting.")
                    car.stop()
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        car.stop()
        Vilib.camera_close()

if __name__ == "__main__":
    main()
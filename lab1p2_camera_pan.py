from picarx import Picarx
import time
import random

# global variable for car speed
SPEED = 50
# threshhold of object distance
OBJECT_CLOSE = 20

def main():
    try:
        px = Picarx()
        # keep moving
        pan_angle = -60
        px.set_cam_pan_angle(pan_angle)
        for i in range(0, 12):
            time.sleep(0.5)
            pan_angle = pan_angle + 10
            px.set_cam_pan_angle(pan_angle)

    finally:
        px.stop()
    
if __name__ == "__main__":
    main()
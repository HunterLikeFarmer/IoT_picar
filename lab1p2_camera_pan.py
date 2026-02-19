from picarx import Picarx
import time
import random
import numpy as np

# global variable for car speed
SPEED = 50
# threshhold of object distance
OBJECT_CLOSE = 20

ARRAY_HEIGHT = 20
ARRAY_WIDTH = 20

object_array = np.zeros((ARRAY_WIDTH, ARRAY_HEIGHT))

def main():
    try:
        px = Picarx()
        # keep moving
        pan_angle = -90
        px.set_cam_pan_angle(pan_angle)
        for i in range(0, 90):
            time.sleep(0.1)
            pan_angle = pan_angle + 2
            px.set_cam_pan_angle(pan_angle)
            d = round(px.ultrasonic.read(), 2)
            if (d > 0):
                object_array[round(d * np.cos(pan_angle)) + 10, round(d * np.sin(pan_angle)) + 0] = 1
        time.sleep(0.1)
        px.set_cam_pan_angle(0)
        for i in range (0, ARRAY_HEIGHT):
            print("\n")
            for j in range (0, ARRAY_WIDTH):
                print(object_array[j,i])

    finally:
        px.stop()
    
if __name__ == "__main__":
    main()
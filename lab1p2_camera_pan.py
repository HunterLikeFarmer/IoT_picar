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
            d = round(px.ultrasonic.read() / 10, 2)
            if (d > 0):
                print((d, pan_angle))
                x_val = round(d * np.cos(pan_angle)) + 10
                y_val = round(d * np.sin(pan_angle)) + 0
                if (x_val < 0 or x_val >= 20 or y_val < 0 or y_val >= 20):
                    continue
                print("Added to: ", (x_val, y_val))
                object_array[y_val, x_val] = 1
        time.sleep(0.1)
        px.set_cam_pan_angle(0)
        print(object_array)

    finally:
        px.stop()
    
if __name__ == "__main__":
    main()
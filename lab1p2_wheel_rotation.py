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

        for i in range(0, 10):
            px.set_dir_servo_angle(10)
            px.backward(SPEED)
            time.sleep(0.25)
            px.set_dir_servo_angle(0)
            px.forward(SPEED)
            time.sleep(0.25)

    finally:
        px.stop()
    
if __name__ == "__main__":
    main()
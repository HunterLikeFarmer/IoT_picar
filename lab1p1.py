from picarx import Picarx
import time
import random

# global variable for car speed
SPEED = 25
# threshhold of object distance
OBJECT_CLOSE = 20

def main():
    try:
        px = Picarx()
        # keep moving
        while True:
            d = round(px.ultrasonic.read(), 2)
            print(d)
            # when the object is at sight
            if d <= OBJECT_CLOSE and d > 0:
                # stop the car
                px.stop()
                time.sleep(0.5)
                # turn to either left or right 
                if random.randint(0, 1) == 0:
                    px.set_dir_servo_angle(-40)
                else:
                    px.set_dir_servo_angle(30)
                # go back
                px.backward(SPEED)
                time.sleep(1)
                px.stop()
            # when it no obstacles in sight: move forward
            else:
                px.set_dir_servo_angle(0)
                px.forward(SPEED)


    finally:
        px.stop()
    
if __name__ == "__main__":
    main()
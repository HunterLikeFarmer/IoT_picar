from picarx import Picarx
import time
import random

SPEED = 75
OBJECT_CLOSE = 20

def main():
    try:
        px = Picarx()
        while True:
            d = round(px.ultrasonic.read(), 2)
            print(d)
            if d <= OBJECT_CLOSE:
                px.stop()
                time.sleep(0.5)
                px.backward(SPEED)
                time.sleep(1)
                px.stop()
                if random.randint(0, 1) == 0:
                    px.set_dir_servo_angle(-30)
                else:
                    px.set_dir_servo_angle(30)
                px.forward(SPEED)



    finally:
        px.stop()
    
if __name__ == "__main__":
    main()
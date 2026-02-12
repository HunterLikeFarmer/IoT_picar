import picar_4wd as fc
import time
import random

speed = 30

BACK_TIME = 0.45
TURN_TIME = 0.55
STOP_TIME = 0.05

# check if theres an obstacle
def blocked(scan_list):
    front = scan_list[3:7]
    return front != [2, 2, 2, 2]

def change_dir():
    fc.stop()
    time.sleep(STOP_TIME)

    # back up
    fc.backward(speed)
    time.sleep(BACK_TIME)
    fc.stop()
    time.sleep(STOP_TIME)

    # choose random direction
    if random.choice([True, False]):
        fc.turn_left(speed)
    else:
        fc.turn_right(speed)
    time.sleep(TURN_TIME)
    fc.stop()
    time.sleep(STOP_TIME)

def main():
    while True:
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue
        
        # if blocked
        if blocked(scan_list):
            change_dir()
        # else keep going forward
        else:
            fc.forward(speed)

        time.sleep(0.05)

if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()
        time.sleep(0.2)

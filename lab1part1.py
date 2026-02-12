import picar_4wd as fc
import time
import random

speed = 30

BACK_SLEEP = 0.45
TURN_SLEEP = 0.55
STOP_SLEEP = 0.05

# check if theres an obstacle
def blocked(scan_list):
    return scan_list[3:7] != [2, 2, 2, 2]

def change_dir():
    fc.stop()
    time.sleep(STOP_SLEEP)

    # back up
    fc.backward(speed)
    time.sleep(BACK_SLEEP)
    fc.stop()
    time.sleep(STOP_SLEEP)

    # choose random direction
    if random.choice([True, False]):
        fc.turn_left(speed)
    else:
        fc.turn_right(speed)
    time.sleep(TURN_SLEEP)
    fc.stop()
    time.sleep(STOP_SLEEP)

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

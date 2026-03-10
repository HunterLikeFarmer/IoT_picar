import numpy as np
import time

#Picar Library
from picarx import Picarx
from vilib import Vilib

#Custom Libraries
from motion import execute_path
from scan import scan_environment, add_clearance
from algo import astar
from stop_scan import scan_for_stop
from params import GRID_HEIGHT, GRID_WIDTH

#COL, ROW
START_POS = (0, 0)
GOAL_POS = (0, GRID_HEIGHT - 1)

def main():
    px = Picarx()
    current_heading = 0
    current_pos = START_POS
    visited_pos = {current_pos}
    visited_block = set()
    raw_grid = None
    safe_grid = None
    stop_recent = 0

    print("Starting camera for Stop Sign detection")
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=True, web=True)
    time.sleep(2)

    while True:
        time.sleep(1)
        scan_for_stop()


if __name__ == "__main__":
    main()
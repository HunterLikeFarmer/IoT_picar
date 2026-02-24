import numpy as np
import time

#Picar Library
from picarx import Picarx

#Custom Libraries
from motion import execute_path
from scan import scan_environment, connect_point, add_clearance
from algo import astar
from stop_scan import scan_for_stop
from params import GRID_HEIGHT, GRID_WIDTH

#COL, ROW
START_POS = (5, 0)
GOAL_POS = (5, 9)

def main():
    px = Picarx()
    visited_block = set()
    current_pos = (0, 0)
    current_heading = 0
    visited_pos = {current_pos}
    scan_environment(px, current_pos, current_heading, visited_pos, visited_block)
    current_pos = (1, 0)
    current_heading = 90
    time.sleep(5)
    scan_environment(px, current_pos, current_heading, visited_pos, visited_block)
    #ADD NEXT VISITED POS
                


if __name__ == "__main__":
    main()
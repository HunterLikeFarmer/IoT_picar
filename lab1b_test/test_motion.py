import numpy as np
import time

#Picar Library
from picarx import Picarx
from vilib import Vilib

#Custom Libraries
from motion import execute_path
#from scan import scan_environment, connect_point, add_clearance
from algo import astar
from stop_scan import scan_for_stop
from params import GRID_HEIGHT, GRID_WIDTH

#COL, ROW
START_POS = (5, 0)
GOAL_POS = (5, 9)

def main():
    px = Picarx()
    current_heading = 0
    current_heading = execute_path(px, (0, 0), (1, 0), current_heading)
    #current_heading = execute_path(px, (0, 0), (0, -1), current_heading)
    #current_heading = execute_path(px, (0, 0), (0, -1), current_heading)
    #current_heading = execute_path(px, (0, 0), (0, -1), current_heading)
                


if __name__ == "__main__":
    main()
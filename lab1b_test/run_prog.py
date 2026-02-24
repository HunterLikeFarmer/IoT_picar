import numpy as np
import time

#Picar Library
from picarx import Picarx
from vilib import Vilib

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
    current_heading = 0
    current_pos = START_POS
    visited_pos = {current_pos}
    raw_grid = np.zeros((10, 10))
    safe_grid = np.zeros((10, 10))
    step_count = 0

    print("Starting camera for Stop Sign detection")
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=True, web=True)
    time.sleep(2)

    try:
        while current_pos != GOAL_POS:

            raw_grid = scan_environment(px, current_pos)
            safe_grid = connect_point(raw_grid)
            #safe_grid = add_clearance(raw_grid, 1)
            print(raw_grid)
            #print(safe_grid)

            path = astar(safe_grid, current_pos, GOAL_POS)

            if not path:
                print("No safe path to goal! Path completely blocked.")
                px.stop()
                break

            for i in range (len(path)):
                next_pos = path[i]
                
                # Execute step and update our heading state
                current_heading = execute_path(px, next_pos, current_pos, current_heading)
                if (scan_for_stop()):
                    time.sleep(3)
                
                current_pos = next_pos
                visited_pos.add(current_pos)

                step_count = (step_count + 1) % 3
                if (step_count == 2):
                    print("SCAN!!")

    except KeyboardInterrupt:
        print("Self-Driving aborted by user.")
    finally:
        px.stop()
        Vilib.camera_close()


if __name__ == "__main__":
    main()
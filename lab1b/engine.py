"""Self-driving engine entrypoint, split across helper modules."""

import time

from picarx import Picarx
from vilib import Vilib

from algo import astar
from config import CAR_POS, CLEARANCE_RADIUS, GOAL_POS, GRID_HEIGHT
from motion import execute_path_step
from utils import add_clearance, connect_point, scan_environment


def main():
    px = Picarx()
    current_pos = CAR_POS

    visited_positions = {current_pos}

    print("Starting camera for Stop Sign and Pedestrian detection...")
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=True)
    time.sleep(2)

    Vilib.color_detect("red")
    Vilib.face_detect_switch(True)

    last_stop_time = 0

    try:
        while current_pos != GOAL_POS:
            if Vilib.detect_obj_parameter.get("color_n", 0) != 0:
                if Vilib.detect_obj_parameter.get("color_w", 0) > 40:
                    if time.time() - last_stop_time > 10:
                        print("Stop sign detected. Stop for 3s")
                        px.stop()
                        time.sleep(3)
                        print("Proceeding...")
                        last_stop_time = time.time()

            raw_grid = scan_environment(px, current_pos, visited_positions)
            raw_grid = connect_point(raw_grid)

            if Vilib.detect_obj_parameter.get("human_n", 0) != 0:
                print("Human (pedestrian) detected! Forcing route around them.")
                human_x = current_pos[0]
                human_y = min(GRID_HEIGHT - 1, current_pos[1] + 3)
                raw_grid[human_y, human_x] = 1

            safe_grid = add_clearance(raw_grid, radius=CLEARANCE_RADIUS)
            path = astar(safe_grid, current_pos, GOAL_POS)

            if not path:
                print("No safe path to goal! Path completely blocked.")
                px.stop()
                break

            print(f"Path found. Executing next steps: {path[:2]}")

            steps_to_take = min(2, len(path))
            for i in range(steps_to_take):
                next_pos = path[i]
                execute_path_step(px, next_pos, current_pos)
                current_pos = next_pos
                visited_positions.add(current_pos)

        if current_pos == GOAL_POS:
            print("Successfully reached the destination!")

    except KeyboardInterrupt:
        print("Self-Driving aborted by user.")
    finally:
        px.stop()
        Vilib.camera_close()


if __name__ == "__main__":
    main()

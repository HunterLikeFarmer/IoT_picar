import time
import heapq
import numpy as np
from picarx import Picarx
from vilib import Vilib

from params import GRID_HEIGHT, GRID_WIDTH

# global variable
# GRID_WIDTH = 30
# GRID_HEIGHT = 30
#CAR_POS = (GRID_WIDTH / 2, 0)  # Car starts at top-center
#GOAL_POS = (GRID_WIDTH / 2, 25) # Goal is straight ahead
# CLEARANCE_RADIUS = 1
# STEP_TIME = 0.5  
# SPEED = 30


# visited block is a tuple
def scan_environment(px, current_pos, current_heading, visited_pos, visited_block):
    print("Scanning environment...")
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))
    
    for angle in range(-60, 60, 5): # Scan every 5 degrees
        px.set_cam_pan_angle(angle)
        time.sleep(0.1)
        
        distance = px.get_distance()
        d_grid = distance
        
        if 0 < d_grid < GRID_HEIGHT * 10:
            # print(d_grid)
            absolute_angle = angle + current_heading
            rad = np.radians(absolute_angle)
            x_val = int(round(d_grid * np.sin(rad)) / 10) + current_pos[0] 
            y_val = int(round(d_grid * np.cos(rad)) / 10) + current_pos[1] 
            
            if 0 <= x_val < GRID_WIDTH and 0 <= y_val < GRID_HEIGHT:
                grid[y_val, x_val] = 1
                #visited_block.add((y_val, x_val))
    #connect_point(grid)
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if grid[i, j] == 1:
                visited_block.add((i, j))
            
    px.set_cam_pan_angle(0) # Reset camera forward for Vilib
    time.sleep(0.2)
    # print(grid)
    for vx, vy in visited_pos:
        if 0 <= vx < GRID_WIDTH and 0 <= vy < GRID_HEIGHT:
            if grid[vy, vx] == 0:
                grid[vy, vx] = 2
    for vy, vx in visited_block:
        grid[vy, vx] = 1
        
    return grid

def connect_point(grid):
    to_change = []
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            count_one = 0
            x_arr = [-1, 0, 1]
            y_arr = [-1, 0, 1]
            for x in x_arr:
                for y in y_arr:
                    if x == 0 and y == 0:
                        continue
                    cur_x = i + x
                    cur_y = j + y
                    if cur_x >= 0 and cur_y >= 0 and cur_x < GRID_HEIGHT and cur_y < GRID_WIDTH and grid[cur_y, cur_x] == 1:
                        count_one += 1
            if count_one >= 2:
                to_change.append((j, i))
    for tup in to_change:
        x, y = tup
        grid[x, y] = 1
    return grid

def add_clearance(grid, radius=1):
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:
                r_min, r_max = max(0, r - radius), min(rows, r + radius + 1)
                c_min, c_max = max(0, c - radius), min(cols, c + radius + 1)
                new_grid[r_min:r_max, c_min:c_max] = 1
    return new_grid
    
            
                    
            
                
            
                

#if __name__ == "__main__":
#    px = Picarx()
#    
#    grid = scan_environment(px, CAR_POS)
#    print("Original Grid: ")
#    print(grid)
#    print("Connected Grid: \n")
#    print(connect_point(grid))
    
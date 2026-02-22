import time
import heapq
import numpy as np
from picarx import Picarx
from vilib import Vilib


# global variable
GRID_WIDTH = 30
GRID_HEIGHT = 30
CAR_POS = (GRID_WIDTH // 2, 0)  # Car starts at bottom-center
GOAL_POS = (GRID_WIDTH // 2, 25) # Goal is straight ahead
CLEARANCE_RADIUS = 2  
STEP_TIME = 0.5  
SPEED = 30



def scan_environment(px, current_pos):
    print("Scanning environment...")
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    
    for angle in range(-60, 61, 15): # Scan every 15 degrees to speed it up
        px.set_cam_pan_angle(angle)
        time.sleep(0.05)
        
        distance = px.get_distance()
        d_grid = round(distance / 5.0) 
        
        if 0 < d_grid < GRID_HEIGHT:
            print(d_grid)
            rad = np.radians(angle)
            x_val = int(round(d_grid * np.sin(rad))) + current_pos[0] 
            y_val = int(round(d_grid * np.cos(rad))) + current_pos[1] 
            
            if 0 <= x_val < GRID_WIDTH and 0 <= y_val < GRID_HEIGHT:
                grid[y_val, x_val] = 1
                
    px.set_cam_pan_angle(0) # Reset camera forward for Vilib
    time.sleep(0.2)
    print(grid)
    return grid

if __name__ == "__main__":
    px = Picarx()
    
    scan_environment(px, CAR_POS)
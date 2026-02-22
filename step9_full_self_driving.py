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

# A* Pathfinding Algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    neighbors = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            
            if not (0 <= neighbor[0] < grid.shape[1] and 0 <= neighbor[1] < grid.shape[0]):
                continue
            if grid[neighbor[1], neighbor[0]] == 1:
                continue

            tentative_g_score = gscore[current] + 1
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
                
    return None

# Mapping and obstacle processing
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

def scan_environment(px, current_pos):
    print("Scanning environment...")
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    
    for angle in range(-60, 61, 15): # Scan every 15 degrees to speed it up
        px.set_cam_pan_angle(angle)
        time.sleep(0.05)
        
        distance = px.get_distance()
        d_grid = round(distance / 5.0) 
        
        if 0 < d_grid < GRID_HEIGHT:
            rad = np.radians(angle)
            x_val = int(round(d_grid * np.sin(rad))) + current_pos[0] 
            y_val = int(round(d_grid * np.cos(rad))) + current_pos[1] 
            
            if 0 <= x_val < GRID_WIDTH and 0 <= y_val < GRID_HEIGHT:
                grid[y_val, x_val] = 1
                
    px.set_cam_pan_angle(0) # Reset camera forward for Vilib
    time.sleep(0.2)
    return grid

# Execution
def execute_path_step(px, next_node, current_node):
    dx = next_node[0] - current_node[0]
    dy = next_node[1] - current_node[1]
    
    if dx > 0:
        px.set_dir_servo_angle(30)
        px.forward(SPEED)
    elif dx < 0:
        px.set_dir_servo_angle(-30)
        px.forward(SPEED)
    elif dy > 0:
        px.set_dir_servo_angle(0)
        px.forward(SPEED)
    elif dy < 0:
        px.set_dir_servo_angle(0)
        px.backward(SPEED)
        
    time.sleep(STEP_TIME)
    px.stop()

# Self driving Loop
def main():
    px = Picarx()
    current_pos = CAR_POS
    
    # 1. Initialize Vilib
    print("Starting camera for Stop Sign and Pedestrian detection...")
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=True)
    time.sleep(2)
    
    # We use color detection to find the Stop Sign (Red)
    Vilib.color_detect("red")
    
    # Enable face detection to look for humans/pedestrians
    Vilib.face_detect_switch(True)
    
    # Cooldown to prevent stopping at the same sign infinitely
    last_stop_time = 0 
    
    try:
        while current_pos != GOAL_POS:
            
            # look for traffic sign
            # If a red object is large enough, and we haven't stopped in the last 10 seconds
            if Vilib.detect_obj_parameter.get('color_n', 0) != 0:
                if Vilib.detect_obj_parameter.get('color_w', 0) > 40:
                    if time.time() - last_stop_time > 10:
                        print("Stop sign detected. Stop for 3s")
                        px.stop()
                        time.sleep(3)
                        print("Proceeding...")
                        last_stop_time = time.time()
                                    
            # mapping and routing check
            raw_grid = scan_environment(px, current_pos) 
            
            # if a sudden pedestrain appears
            if Vilib.detect_obj_parameter.get('human_n', 0) != 0:
                print("Human (pedestrian) detected! Forcing route around them.")
                human_x = current_pos[0]
                human_y = min(GRID_HEIGHT - 1, current_pos[1] + 3) # Assume human is 3 grid units ahead
                raw_grid[human_y, human_x] = 1 # Treat human as a physical wall
            
            safe_grid = add_clearance(raw_grid, radius=CLEARANCE_RADIUS)
            
            path = astar(safe_grid, current_pos, GOAL_POS)
            
            if not path:
                print("No safe path to goal! Path completely blocked.")
                px.stop()
                break
                
            print(f"Path found. Executing next steps: {path[:2]}")
            
            # Follow a couple of steps of the path before rescanning
            steps_to_take = min(2, len(path)) 
            for i in range(steps_to_take):
                
                # Sudden obstacle detection (Dynamic roadblocks)
                # Check immediately before moving
                if px.get_distance() < 15: 
                    print("Sudden obstacle detected! Recalculating route...")
                    px.stop()
                    break # Break out of the execution loop to force an immediate rescan
                
                next_pos = path[i]
                execute_path_step(px, next_pos, current_pos)
                current_pos = next_pos
                
        if current_pos == GOAL_POS:
            print("Successfully reached the destination!")
            
    except KeyboardInterrupt:
        print("Self-Driving aborted by user.")
    finally:
        px.stop()
        Vilib.camera_close()

if __name__ == "__main__":
    main()
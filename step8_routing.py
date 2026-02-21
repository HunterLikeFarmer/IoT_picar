import time
import heapq
import numpy as np
from picarx import Picarx

GRID_WIDTH = 30
GRID_HEIGHT = 30
CAR_POS = (GRID_WIDTH // 2, 0)  # Car starts at bottom-center of the grid
GOAL_POS = (GRID_WIDTH // 2, 25) # Goal is straight ahead
CLEARANCE_RADIUS = 2  # How many grid cells to inflate obstacles by
STEP_TIME = 0.5  # Seconds to drive for one grid step
SPEED = 30

# A* Pathfinding Algorithm
def heuristic(a, b):
    # distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    # Finds the shortest path from start to goal on a 2D grid.
    # Returns a list of (x, y) coordinates, or None if no path exists.
    # 4 possible moves: Right, Left, Down, Up
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
            
            # Check grid bounds
            if not (0 <= neighbor[0] < grid.shape[1] and 0 <= neighbor[1] < grid.shape[0]):
                continue
            
            # Check for obstacles (1 = obstacle)
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

# Mapping and Obstacle Processing
def add_clearance(grid, radius=1):
    # Inflates obstacles by a given radius to prevent the car from scraping
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:
                # Add 1 around the obstacle
                r_min, r_max = max(0, r - radius), min(rows, r + radius + 1)
                c_min, c_max = max(0, c - radius), min(cols, c + radius + 1)
                new_grid[r_min:r_max, c_min:c_max] = 1
    return new_grid

def scan_environment(px):
    # Generates a map of the surroundings.
    print("Scanning...")
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    px.set_cam_pan_angle(-60)
    time.sleep(0.3)
    
    for angle in range(-60, 61, 10):
        px.set_cam_pan_angle(angle)
        time.sleep(0.05)
        
        distance = px.get_distance()
        d_grid = round(distance / 5.0) # 1 grid unit = 5 cm
        
        if 0 < d_grid < GRID_HEIGHT:
            rad = np.radians(angle)
            x_val = int(round(d_grid * np.sin(rad))) + CAR_POS[0]
            y_val = int(round(d_grid * np.cos(rad))) + CAR_POS[1]
            
            if 0 <= x_val < GRID_WIDTH and 0 <= y_val < GRID_HEIGHT:
                grid[y_val, x_val] = 1
                
    px.set_cam_pan_angle(0)
    return grid

# Execution
def execute_path_step(px, next_node, current_node):
    # translates the next grid coordinate into physical car movement
    dx = next_node[0] - current_node[0]
    dy = next_node[1] - current_node[1]
    
    if dx > 0:
        print("  Turning Right")
        px.set_dir_servo_angle(30)
        px.forward(SPEED)
    elif dx < 0:
        print("  Turning Left")
        px.set_dir_servo_angle(-30)
        px.forward(SPEED)
    elif dy > 0:
        print("  Moving Forward")
        px.set_dir_servo_angle(0)
        px.forward(SPEED)
    elif dy < 0:
        print("  Reversing")
        px.set_dir_servo_angle(0)
        px.backward(SPEED)
        
    time.sleep(STEP_TIME)
    px.stop()

# Main Routing Loop
def main():
    px = Picarx()
    current_pos = CAR_POS
    
    try:
        while current_pos != GOAL_POS:
            # 1. Scan and add anti-scraping inflation
            raw_grid = scan_environment(px)
            safe_grid = add_clearance(raw_grid, radius=CLEARANCE_RADIUS)
            
            # 2. Calculate A* Path
            path = astar(safe_grid, current_pos, GOAL_POS)
            
            if not path:
                print("No safe path to goal! Obstacles are blocking the way.")
                break
                
            print(f"Path found. Next steps: {path[:3]}")
            
            # 3. Follow the first few steps of the path before rescanning
            steps_to_take = min(2, len(path)) # Move 2 steps, then rescan
            for i in range(steps_to_take):
                next_pos = path[i]
                execute_path_step(px, next_pos, current_pos)
                current_pos = next_pos
                
            print(f"Arrived at intermediate position: {current_pos}")
            time.sleep(0.5)
            
        if current_pos == GOAL_POS:
            print("Successfully reached the destination!")
            
    except KeyboardInterrupt:
        print("Navigation aborted.")
    finally:
        px.stop()

if __name__ == "__main__":
    main()
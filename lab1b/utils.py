"""Grid utilities and environment scanning."""

import time
import numpy as np

from config import GRID_WIDTH, GRID_HEIGHT


def connect_point(grid):
    to_change = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            count_one = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue

                    cur_y = y + dy
                    cur_x = x + dx

                    if 0 <= cur_y < GRID_HEIGHT and 0 <= cur_x < GRID_WIDTH:
                        if grid[cur_y, cur_x] == 1:
                            count_one += 1

            if count_one >= 2:
                to_change.append((y, x))

    for y, x in to_change:
        grid[y, x] = 1

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


def scan_environment(px, current_pos, visited_positions):
    print("Scanning environment...")
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)

    # Scan every 15 degrees to speed up mapping.
    for angle in range(-60, 61, 15):
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

    px.set_cam_pan_angle(0)
    time.sleep(0.2)

    # Mark traversed coordinates as 2 unless now occupied by an obstacle.
    for vx, vy in visited_positions:
        if 0 <= vx < GRID_WIDTH and 0 <= vy < GRID_HEIGHT:
            if grid[vy, vx] == 0:
                grid[vy, vx] = 2

    print(grid)
    return grid

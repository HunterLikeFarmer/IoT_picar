#!/usr/bin/env python3
"""
Turn test using execute_path_step() from your motion helpers.

This simulates a path:
    forward → right → forward → left → repeat

So the car repeatedly performs left/right arcs using the same logic as Part 9.
"""

import time
from picarx import Picarx

# Import your motion helper
from motion import execute_path_step

# -------------------------
# Test parameters
# -------------------------
START_POS = (10, 10)
LOOPS = 20        # set None for infinite loop
PAUSE = 0.5       # pause between steps

# Directions to test (relative grid moves)
TEST_MOVES = [
    (0, 1),   # forward (North)
    (1, 0),   # right turn (East)
    (0, 1),   # forward
    (-1, 0),  # left turn (West)
]

def main():
    px = Picarx()
    px.set_dir_servo_angle(0)
    px.stop()

    current_pos = START_POS
    current_heading = 0  # 0 = North

    print("Starting execute_path_step turn test.")
    print("Press Ctrl+C to stop.\n")

    step_count = 0

    try:
        while True:
            for dx, dy in TEST_MOVES:
                next_pos = (current_pos[0] + dx, current_pos[1] + dy)

                print(f"\nStep {step_count}: {current_pos} → {next_pos}")
                print(f"Heading before: {current_heading}")

                current_heading = execute_path_step(
                    px,
                    next_pos,
                    current_pos,
                    current_heading
                )

                print(f"Heading after: {current_heading}")

                current_pos = next_pos
                step_count += 1
                time.sleep(PAUSE)

            if LOOPS is not None and step_count >= LOOPS:
                print("\nTest complete.")
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        px.set_dir_servo_angle(0)
        px.stop()

if __name__ == "__main__":
    main()
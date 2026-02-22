"""Vehicle motion helpers."""

import time

from config import SPEED, STEP_TIME


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

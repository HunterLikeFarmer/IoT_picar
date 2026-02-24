"""Vehicle motion helpers."""

import time

from config import SPEED, STEP_TIME


def execute_path_step(px, next_node, current_node, current_heading):
    dx = next_node[0] - current_node[0]
    dy = next_node[1] - current_node[1]

    # 1. Determine the target heading based on grid movement
    if dy > 0: target_heading = 0      # North / Up
    elif dx > 0: target_heading = 90   # East / Right
    elif dy < 0: target_heading = 180  # South / Down
    elif dx < 0: target_heading = 270  # West / Left
    else: target_heading = current_heading

    # Calculate how much we need to change our heading
    turn_angle = (target_heading - current_heading) % 360

    # WARNING: You will need to physically tune these time variables.
    ARC_TIME_FWD = 1.0  # The "bit longer" forward arc
    ARC_TIME_BWD = 0.4  # The "short while" backward correction

    if turn_angle == 90:
        print("Steering Right...")
        # 1. Turn and move forward for a bit longer
        px.set_dir_servo_angle(30)   # Set wheel direction right
        px.forward(SPEED)            # Go forward
        time.sleep(ARC_TIME_FWD * 4)      
        
        # 2. Straighten wheels and go backward for a short while
        px.set_dir_servo_angle(0)    
        px.backward(SPEED)           
        time.sleep(ARC_TIME_BWD * 3)     
        
    elif turn_angle == 270:
        print("Steering Left...")
        # 1. Turn and move forward for a bit longer
        px.set_dir_servo_angle(-30)  # Set wheel direction left
        px.forward(SPEED)            # Go forward
        time.sleep(ARC_TIME_FWD * 3.2)     
        
        # 2. Straighten wheels and go backward for a short while
        px.set_dir_servo_angle(0)    
        px.backward(SPEED)           
        time.sleep(ARC_TIME_BWD*3)     
        
    elif turn_angle == 180:
        print("U-Turn Arc...")
        px.set_dir_servo_angle(30)   # Set wheel direction right
        px.forward(SPEED)            
        time.sleep(ARC_TIME_FWD * 8) # Drive twice as long to complete a 180
        
        # Optional backward correction for the U-turn
        px.set_dir_servo_angle(0)    
        px.backward(SPEED)           
        time.sleep(ARC_TIME_BWD * 4)     
        
    else: # turn_angle == 0
        print("Driving Straight...")
        px.set_dir_servo_angle(0)    # Keep wheels straight
        px.forward(SPEED)
        time.sleep(STEP_TIME)        # Drive straight into the next cell

    px.stop()
    
    return target_heading
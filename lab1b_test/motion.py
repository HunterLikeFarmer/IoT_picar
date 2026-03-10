import time

SPEED = 12
FORWARD_TIME = 0.95

TURN_TIME_LEFT = 1
TURN_BACK_TIME_LEFT = 1.2

TURN_TIME_RIGHT = 3.6
TURN_BACK_TIME_RIGHT = 1.4

TURN_TIME_U = 2
TURN_TIME_U_2 = 1

def execute_path(px, next_node, current_node, current_heading):
    new_x = next_node[0] - current_node[0]
    new_y = next_node[1] - current_node[1]

    new_heading = 0
    if new_y == 0 and new_x != 0:
        if new_x < 0: 
            new_heading = 90
        elif new_x > 0: 
            new_heading = -90
    elif new_x == 0 and new_y != 0:
        if new_y > 0: 
            new_heading = 0
        elif new_y < 0: 
            new_heading = 180
    else:
        print("Error in Next Node: ", new_x, new_y)

    turn_angle = (new_heading - current_heading) % 360
    
    if turn_angle == 0:
        print("Moving Forward")
        px.set_dir_servo_angle(3)
        px.forward(SPEED)
        time.sleep(FORWARD_TIME)
    elif turn_angle == 90:
        print("Turning Right")
        px.set_dir_servo_angle(60)
        px.forward(SPEED)
        time.sleep(TURN_TIME_RIGHT)
        px.set_dir_servo_angle(-60)
        px.backward(SPEED)
        time.sleep(TURN_BACK_TIME_RIGHT)
        px.set_dir_servo_angle(0)
        px.forward(SPEED)
        time.sleep(FORWARD_TIME * 2.2)
    elif turn_angle == 270:
        print("Turning Left")
        px.set_dir_servo_angle(-60)
        px.forward(SPEED)
        time.sleep(TURN_TIME_LEFT)
        px.set_dir_servo_angle(60)
        px.backward(SPEED)
        time.sleep(TURN_BACK_TIME_LEFT)
        px.set_dir_servo_angle(0)
        px.forward(SPEED)
        time.sleep(FORWARD_TIME * 1.4)
        
    elif turn_angle == 180:
        print("U-TURN")
        px.set_dir_servo_angle(-60)
        px.forward(SPEED)
        time.sleep(TURN_TIME_U)
        px.set_dir_servo_angle(60)
        px.backward(SPEED)
        time.sleep(TURN_TIME_U)
        px.set_dir_servo_angle(-60)
        px.forward(SPEED)
        time.sleep(0.3)
        px.set_dir_servo_angle(0)
        px.forward(SPEED)
        time.sleep(TURN_TIME_U * 1.1)

    px.set_dir_servo_angle(0)
    px.stop()

    return new_heading

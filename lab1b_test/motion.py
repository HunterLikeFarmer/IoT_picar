import time

SPEED = 15
FORWARD_TIME = 0.7

TURN_TIME_LEFT = 1.3
TURN_BACK_TIME_LEFT = 0.9

TURN_TIME_RIGHT = 1.9
TURN_BACK_TIME_RIGHT = 2.4
TURN_BACK_TIME_RIGHT_D = 2.6

TURN_TIME_U = 2
TURN_TIME_U_2 = 1

def execute_path(px, next_node, current_node, current_heading):
    new_x = next_node[0] - current_node[0]
    new_y = next_node[1] - current_node[1]

    new_heading = 0
    if new_y == 0 and new_x != 0:
        if new_x < 0: new_heading = 90
        elif new_x > 0: new_heading = -90
    elif new_x == 0 and new_y != 0:
        if new_y > 0: new_heading = 0
        elif new_y < 0: new_heading = 180
    else:
        print("Error in Next Node: ", new_x, new_y)

    turn_angle = (new_heading - current_heading) % 360
    
    if turn_angle == 0:
        print("Moving Forward")
        px.set_dir_servo_angle(-0.5)
        px.forward(SPEED)
        time.sleep(FORWARD_TIME)
    elif turn_angle == 90:
        print("Turning Right")
        px.set_dir_servo_angle(-60)
        px.backward(SPEED)
        time.sleep(TURN_BACK_TIME_RIGHT)
        px.set_dir_servo_angle(60)
        px.forward(SPEED)
        time.sleep(TURN_TIME_RIGHT)
        px.set_dir_servo_angle(-60)
        px.backward(SPEED)
        time.sleep(TURN_BACK_TIME_RIGHT_D)
        px.set_dir_servo_angle(0)
        px.forward(SPEED)
        time.sleep(FORWARD_TIME)
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
        time.sleep(FORWARD_TIME)
        
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
        time.sleep(TURN_TIME_U_2)
        px.set_dir_servo_angle(0)
        px.forward(SPEED)
        time.sleep(TURN_TIME_U_2)

    px.set_dir_servo_angle(0)
    px.stop()

    return new_heading

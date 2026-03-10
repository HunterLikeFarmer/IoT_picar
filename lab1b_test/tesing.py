import socket
import math
import numpy as np
import time
from picarx import Picarx
from vilib import Vilib
from stop_scan import scan_for_stop
from motion import execute_path
from power_read import get_battery_voltage
from params import GRID_HEIGHT, GRID_WIDTH
from scan import scan_environment, add_clearance

HOST = "192.168.10.6" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
current_heading = 0
x_pos = 0
y_pos = 0



if __name__ == "__main__":
    px = Picarx()
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=True, web=True)
    time.sleep(2)
    send_data = f"{current_heading};{scan_for_stop()};{math.sqrt((x_pos)**2 + (y_pos)**2)};{get_battery_voltage()}"
    print(send_data)
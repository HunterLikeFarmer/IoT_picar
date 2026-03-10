import socket
import math
import time
from picarx import Picarx
from vilib import Vilib
from stop_scan import scan_for_stop
from motion import execute_path
from power_read import get_battery_voltage

HOST = "192.168.10.6" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
current_heading = 0
x_pos = 0
y_pos = 0

px = Picarx()
Vilib.camera_start(vflip=False, hflip=False)
Vilib.display(local=True, web=True)
time.sleep(2)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)
                # client.sendall(data) # Echo back to client
                match data: 
                    case b"87\r\n":
                        #Forward
                        print("Moving Forward")
                        execute_path(px, (0, 0), (0, -1), 0)
                        y_pos += 1
                    case b"65\r\n":
                        #Left
                        print("Moving Left")
                        execute_path(px, (0, 0), (-1, 0), 0)
                        current_heading = (current_heading - 90)
                        x_pos -= 1
                    case b"68\r\n":
                        #Right
                        print("Moving Right")
                        execute_path(px, (0, 0), (1, 0), 0)
                        current_heading = (current_heading + 90)
                        x_pos += 1
                    case b"83\r\n":
                        #Back
                        print("Moving Back")
                        execute_path(px, (0, 0), (0, 1), 0)
                        y_pos -= 1
                    case _:
                        print(data)
                    
                if (current_heading == 270):
                    current_heading = -90
                elif (current_heading == -270):
                    current_heading = 90
                send_data = f"{current_heading};{scan_for_stop()};{round(math.sqrt((x_pos)**2 + (y_pos)**2), 2)};{round(get_battery_voltage(), 2)}"
                client.sendall(send_data.encode("utf-8"))
                print(send_data)
                print(f"{x_pos}, {y_pos}")
                        
                        
    except: 
        print("Closing socket")
        client.close()
        s.close()    
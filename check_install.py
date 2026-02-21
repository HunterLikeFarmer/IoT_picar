import sys
import subprocess
import importlib.util

def check_module(module_name, install_cmd):
    # Check if a Python module is accessible
    if importlib.util.find_spec(module_name):
        print(f"Yes Python : {module_name:<10} | Installed")
    else:
        print(f"No Python : {module_name:<10} | MISSING -> Run: {install_cmd}")

def check_system(cmd_name, install_cmd):
    # Check if a system command exists in the PATH
    try:
        subprocess.run(["which", cmd_name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Yes System : {cmd_name:<10} | Installed")
    except subprocess.CalledProcessError:
        print(f"No System : {cmd_name:<10} | MISSING -> Run: {install_cmd}")

def check_i2c():
    # Verify I2C bus is active (required for PiCar-X hat)
    try:
        result = subprocess.run(["ls /dev/i2c-*"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"Yes Hardware: I2C Bus    | Active")
        else:
            print(f"No Hardware: I2C Bus    | MISSING -> Enable via 'sudo raspi-config' (Interface Options > I2C)")
    except Exception:
        pass

print("="*75)
print(f"Still looking, System Dependency Check (Python {sys.version.split()[0]} - Debian Trixie)")
print("="*75)

# 1. System-Level Tools
print("\n--- System Tools ---")
check_system("i2cdetect", "sudo apt install i2c-tools")
check_system("rpicam-jpeg", "sudo apt install rpicam-apps")

# 2. Hardware Interfaces
print("\n--- Hardware Interfaces ---")
check_i2c()

# 3. Standard & Core Python Libraries
print("\n--- Core Python Libraries ---")
check_module("numpy", "sudo apt install python3-numpy")
check_module("cv2", "sudo apt install python3-opencv")
check_module("smbus2", "sudo pip3 install smbus2 --break-system-packages")

# 4. PiCar-X Specific Libraries
print("\n--- PiCar-X Libraries ---")
# The lab manual explicitly recommends vilib for PiCar-X object detection.
check_module("vilib", "git clone https://github.com/sunfounder/vilib.git && cd vilib && sudo pip3 install . --break-system-packages")
# PiCar-X main control library
check_module("picarx", "git clone https://github.com/sunfounder/picar-x.git && cd picar-x && sudo pip3 install . --break-system-packages")
# Robot-hat is a dependency for PiCar-X
check_module("robot_hat", "git clone https://github.com/sunfounder/robot-hat.git && cd robot-hat && sudo pip3 install . --break-system-packages")

print("="*75)
print("Note: If a SunFounder setup.py script fails due to the pip upgrade error, edit the")
print("setup.py file to comment out the 'update pip3' command before running the pip install.")
print("="*75)
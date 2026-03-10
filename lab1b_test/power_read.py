from robot_hat import ADC
import time

def get_battery_voltage():
    bt = ADC("A4")
    value = bt.read()
    vol = value * 3.3 /4095
    battery_vol = vol * 3 / 8.4 * 100
    return battery_vol

if __name__ == "__main__":
    vol = get_battery_voltage()
    print(f"{round(vol, 2)}%")
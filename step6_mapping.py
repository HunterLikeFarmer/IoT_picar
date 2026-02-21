from picarx import Picarx
import time
import numpy as np

def generate_local_map(px, width=20, height=20):
    """
    Scans from -90 to 90 degrees and generates a 2D numpy array map.
    1 represents an obstacle, 0 represents empty space.
    """
    print("Starting environment scan...")
    # Initialize a grid of zeros
    local_map = np.zeros((height, width), dtype=int)
    
    # Start pan angle at -90 (extreme left)
    pan_angle = -90
    px.set_cam_pan_angle(pan_angle)
    time.sleep(0.5) # Wait for servo to move to starting position
    
    # Sweep from -90 to 90 degrees
    for angle in range(-90, 91, 5): # Scan every 5 degrees for efficiency
        px.set_cam_pan_angle(angle)
        time.sleep(0.05) # Give servo time to settle
        
        # Read distance (convert from cm to grid units, e.g., 1 grid unit = 10 cm)
        distance_cm = px.ultrasonic.read()
        d_grid = round(distance_cm / 10.0, 2)
        
        # Ignore errors (-1) and out-of-bounds readings
        if d_grid > 0 and d_grid < height: 
            # Convert polar (distance, angle) to Cartesian (x, y)
            # Note: angle is in degrees, numpy needs radians
            rad = np.radians(angle)
            
            # Assuming car is at (width/2, 0)
            x_val = int(round(d_grid * np.sin(rad))) + (width // 2)
            y_val = int(round(d_grid * np.cos(rad)))
            
            # Mark on map if within bounds
            if 0 <= x_val < width and 0 <= y_val < height:
                local_map[y_val, x_val] = 1
                print(f"Obstacle detected at grid ({x_val}, {y_val})")
                
    # Reset camera to straight forward
    px.set_cam_pan_angle(0)
    return local_map

if __name__ == "__main__":
    try:
        car = Picarx()
        obstacle_map = generate_local_map(car)
        print("\nMap Generated (Car is at the bottom center):")
        # Flip vertically for printing so 'y=0' (the car) is at the bottom
        print(np.flipud(obstacle_map))
    except KeyboardInterrupt:
        print("Canceled.")
    finally:
        car.stop()
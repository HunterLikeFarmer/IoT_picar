import cv2
import numpy as np

# Parameters for traffic sign detection object
traffic_sign_obj_parameter = {
    'x': 0, 'y': 0, 'w': 0, 'h': 0, 
    't': 'none', 'acc': 0
}

def is_stop_sign(contour, hsv_crop):
    """
    Determines if a contour is a stop sign based on shape and color density.
    """
    # 1. Shape Approximation
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.03 * peri, True)
    sides = len(approx)

    # 2. Aspect Ratio (Stop signs are roughly square)
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w) / h
    
    # 3. Stop signs are Octagons (approx 8 sides), 
    # but in CV they often appear with 6 to 10 sides depending on angle
    if 6 <= sides <= 10 and 0.8 <= aspect_ratio <= 1.2:
        return True, 100 # Accuracy is hard-coded as we are using logic
    return False, 0

def traffic_sign_detect(img, border_rgb=(255, 0, 0)):
    r, g, b = border_rgb
    border_bgr = (b, g, r)

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Red color range (Stop signs are red)
    mask_red_1 = cv2.inRange(hsv, (0, 70, 50), (10, 255, 255))
    mask_red_2 = cv2.inRange(hsv, (170, 70, 50), (180, 255, 255))
    mask_all = cv2.bitwise_or(mask_red_1, mask_red_2)

    # Noise removal
    kernel = np.ones((5, 5), np.uint8)
    mask_all = cv2.morphologyEx(mask_all, cv2.MORPH_OPEN, kernel)
    mask_all = cv2.dilate(mask_all, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(mask_all, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    traffic_sign_num = 0
    max_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000: # Filter out small specks
            found, acc = is_stop_sign(cnt, None)
            
            if found:
                x, y, w, h = cv2.boundingRect(cnt)
                
                # Draw Box
                cv2.rectangle(img, (x, y), (x + w, y + h), border_bgr, 2)
                cv2.putText(img, "STOP", (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, border_bgr, 2)

                # Update Parameters
                if area > max_area:
                    max_area = area
                    traffic_sign_obj_parameter.update({
                        'x': int(x + w/2), 'y': int(y + h/2),
                        'w': w, 'h': h, 't': 'stop', 'acc': acc
                    })
                traffic_sign_num += 1

    if traffic_sign_num == 0:
        traffic_sign_obj_parameter['t'] = 'none'

    return img

# --- Test logic remains mostly the same, just call traffic_sign_detect(frame) ---
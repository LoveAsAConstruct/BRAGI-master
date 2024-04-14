import cv2
import time
import os
from parameters import *
def capture_calibration_images(save_path, interval=3, total_images=20, desired_width=1080):
    """
    Captures images at specified intervals from a virtual camera, ensuring no automatic scaling.
    
    Args:
    save_path (str): The directory to save the captured images.
    interval (int): Time in seconds between captures.
    total_images (int): Total number of images to capture.
    desired_width (int): Desired width to capture.
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    cap = cv2.VideoCapture(SOURCE)  # Default camera
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return
    
    # Attempt to set the camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_width)  # Assuming a square frame for simplicity

    print(f"Starting to capture images every {interval} seconds. Press 'q' to quit early.")
    count = 0
    while count < total_images:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break

        if frame.shape[1] != desired_width:
            print(f"Warning: The frame width received ({frame.shape[1]}) does not match the desired width ({desired_width}).")

        filename = f"calibration_{count}_{time.strftime('%Y%m%d-%H%M%S')}.jpg"
        filepath = os.path.join(save_path, filename)
        cv2.imwrite(filepath, frame)
        print(f"Captured image {count+1}/{total_images}: {filepath}")
        count += 1
        time.sleep(interval)

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Usage example
if __name__ == "__main__":
    save_path = 'lens_calibration_images'
    capture_calibration_images(save_path, interval=3, total_images=30, desired_width=1080)

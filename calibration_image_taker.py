import cv2
import time
import os

def capture_calibration_images(save_path, interval=3, total_images=20):
    """
    Captures images at specified intervals and saves them for camera calibration.
    
    Args:
    save_path (str): The directory to save the captured images.
    interval (int): Time in seconds between captures.
    total_images (int): Total number of images to capture.
    """
    # Create the directory if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Start video capture
    cap = cv2.VideoCapture(1)  # Use the default camera
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return
    
    try:
        print(f"Starting to capture images every {interval} seconds. Press 'q' to quit early.")
        count = 0
        while count < total_images:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image.")
                break

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"calibration_{count}_{timestamp}.jpg"
            filepath = os.path.join(save_path, filename)
            cv2.imwrite(filepath, frame)
            print(f"Captured image {count+1}/{total_images}: {filepath}")
            
            count += 1
            time.sleep(interval)  # Wait for the specified interval

            # Display the frame
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Released camera and closed windows.")

# Usage example
save_path = 'lens_calibration_images'
capture_calibration_images(save_path, interval=3, total_images=20)

import cv2
import numpy as np
import pickle
from functions.parameters import *
def load_calibration_parameters(filename=r'flask-app/config/calibration_parameters.pkl'):
    """ Load the saved camera matrix and distortion coefficients. """
    with open(filename, 'rb') as f:
        calibration_data = pickle.load(f)
    return calibration_data['camera_matrix'], calibration_data['dist_coeff']

def undistort_frame(frame, camera_matrix, dist_coeffs, resize = True):
    """ Apply undistortion transformation to a single frame and crop to valid area. """
    h, w = frame.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))  
    undistorted_frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)
    # Crop the image to the ROI to remove the warping at the edges
    x, y, roi_width, roi_height = roi
    undistorted_frame_cropped = undistorted_frame[y:y+roi_height, x:x+roi_width]
    if resize:
        return cv2.resize(undistorted_frame_cropped, (WIDTH, HEIGHT))
    else:
        return undistorted_frame_cropped

def preview_undistorted_video():
    camera_matrix, dist_coeffs = load_calibration_parameters()
    cap = cv2.VideoCapture(SOURCE)

    # Setting camera resolution
    desired_width = WIDTH
    desired_height = HEIGHT
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

    if not cap.isOpened():
        print("Error: Unable to open video source.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to fetch frame from the camera.")
            break

        undistorted_frame = undistort_frame(frame, camera_matrix, dist_coeffs)

        # Resize frames to ensure they are displayed properly
        frame_resized = cv2.resize(frame, (desired_width, desired_height))
        combined_frame = np.hstack((frame_resized, undistorted_frame))
        cv2.imshow("Original | Undistorted", combined_frame)

        if cv2.waitKey(1) == 27:  # Press ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    preview_undistorted_video()

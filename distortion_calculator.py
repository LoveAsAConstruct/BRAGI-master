import cv2
import numpy as np
import glob
import pickle

def calibrate_camera(calibration_images_path, chessboard_size=(7, 7)):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((chessboard_size[1]*chessboard_size[0], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

    objpoints = []
    imgpoints = []

    images = glob.glob(f'{calibration_images_path}/*.jpg')
    images = glob.glob(f'{calibration_images_path}/*.jpg')
    if not images:
        print("No images found. Check the path.")
        return
    print(f"Found {len(images)} images for calibration.")
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)
            cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
            cv2.imshow('Chessboard', img)
            cv2.waitKey(500)
        else:
            print(f"Chessboard not detected in {fname}.")
    cv2.destroyAllWindows()

    if objpoints:
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        print("Calibration successful.")
    else:
        print("Calibration failed. No valid image points collected.")

    # Save the camera matrix and the distortion coefficients
    calibration_data = {'camera_matrix': mtx, 'dist_coeff': dist}
    with open('calibration_parameters.pkl', 'wb') as f:
        pickle.dump(calibration_data, f)

    return mtx, dist

def load_calibration_parameters(filename='calibration_parameters.pkl'):
    with open(filename, 'rb') as f:
        calibration_data = pickle.load(f)
    return calibration_data['camera_matrix'], calibration_data['dist_coeff']

def undistort_image(image, camera_matrix, dist_coeffs):
    h, w = image.shape[:2]
    new_cam_mtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1)
    dst = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_cam_mtx)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst

# Example usage for calibrating and testing undistortion
if __name__ == "__main__":
    calibrate_camera('lens_calibration_images')
    mtx, dist = load_calibration_parameters()
    img = cv2.imread('lens_calibration_images\calibration_2_20240414-142257.jpg')
    undistorted_img = undistort_image(img, mtx, dist)
    cv2.imshow('Undistorted Image', undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

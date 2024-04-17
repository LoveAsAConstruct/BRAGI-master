# detection_module.py

import torch
import cv2
import numpy as np
from lens_correction_stream import *
camera_matrix, dist_coeffs = load_calibration_parameters()
cap = cv2.VideoCapture(SOURCE)

# Setting camera resolution
desired_width = WIDTH
desired_height = HEIGHT
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

if not cap.isOpened():
    print("Error: Unable to open video source.")

def read_frame(undistort = True):
    ret, frame = cap.read()
    if not ret:
        return False, None
    return ret, undistort_frame(frame, camera_matrix, dist_coeffs) if undistort else frame
def load_yolov5_model(weights_path: str = 'yolov5x.pt', device='cuda' if torch.cuda.is_available() else 'cpu'):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path, force_reload=True).to(device)
    model.eval()
    return model

def load_homography_matrix(matrix_path: str = 'homography_matrix.npy'):
    H = np.load(matrix_path)
    return H

def detect_objects(model, frame):
    results = model(frame)
    return results.xyxy[0].cpu().numpy()

def apply_homography_to_bbox(x1, y1, x2, y2, H):
    points = np.array([[x1, y1], [x2, y2]], dtype='float32').reshape(-1, 1, 2)
    new_points = cv2.perspectiveTransform(points, H)
    return int(new_points[0, 0, 0]), int(new_points[0, 0, 1]), int(new_points[1, 0, 0]), int(new_points[1, 0, 1])

def apply_homography_to_point(x, y, H):
    """Applies homography to a single point."""
    point = np.array([[x, y]], dtype='float32').reshape(-1, 1, 2)
    new_point = cv2.perspectiveTransform(point, H)
    return int(new_point[0, 0, 0]), int(new_point[0, 0, 1])


class_names = [
    "person", "bicycle", "car", "motorcycle", "airplane",
    "bus", "train", "truck", "boat", "traffic light",
    "fire hydrant", "stop sign", "parking meter", "bench", "bird",
    "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat",
    "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
    "wine glass", "cup", "fork", "knife", "spoon",
    "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut",
    "cake", "chair", "couch", "potted plant", "bed",
    "dining table", "toilet", "TV", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven",
    "toaster", "sink", "refrigerator", "book", "clock",
    "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

def format_detections(detections, x_offset=0, y_offset=0):
    formatted_detections = []
    #print(f"Detections: {detections.xyxy[0]}")
    for det in detections:

        object_name = class_names[int(det[5])]  # Convert class ID to the corresponding name
        print("detected "+object_name)
        formatted_detections.append({
            "objectName": object_name,
            "confidence": float(det[4]),
            "x1": int(det[0]),
            "y1": int(det[1]),
            "x2": int(det[2]),
            "y2": int(det[3]),
            "center": (int((det[0] + det[2]) / 2), int((det[1] + det[3]) / 2))
        })
    return formatted_detections


def apply_homography(H, image=None, detections=None):
    transformed_image = None
    transformed_detections = []
    if image is not None:
        transformed_image = cv2.warpPerspective(image, H, (image.shape[1], image.shape[0]))
    if detections:
        for det in detections:
            x1, y1, x2, y2 = apply_homography_to_bbox(det['x1'], det['y1'], det['x2'], det['y2'], H)
            center_x, center_y = apply_homography_to_point(det['center'][0], det['center'][1], H)
            transformed_detections.append({
                "objectName": det['objectName'],
                "confidence": det['confidence'],
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "center": (center_x, center_y)
            })
    return transformed_image, transformed_detections


def display_image_with_detections(frame, detections, window_name="Detections"):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, frame.shape[1], frame.shape[0])
    for det in detections:
        cv2.rectangle(frame, (det['x1'], det['y1']), (det['x2'], det['y2']), (0, 255, 0), 2)
        cv2.putText(frame, f"{det['objectName']} {det['confidence']:.2f}", (det['x1'], det['y1'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        center = tuple(int(c) for c in det['center'])  # Convert to tuple of integers if not already
        cv2.circle(frame, center, 5, (0, 0, 255), -1)

    cv2.imshow(window_name, frame)

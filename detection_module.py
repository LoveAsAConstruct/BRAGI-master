# detection_module.py

import torch
import cv2
import numpy as np

# Function to load the YOLOv5 model
def load_yolov5_model(weights_path: str = 'yolov5n.pt'):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path, force_reload=True)
    return model

# Function to load the homography matrix
def load_homography_matrix(matrix_path: str = 'homography_matrix.npy'):
    H = np.load(matrix_path)
    return H

# Function to run detections using YOLOv5
def detect_objects(model, frame):
    results = model(frame)
    return results.xyxy[0].cpu().numpy()  # Converts detections to NumPy array

# Function to format detections
def format_detections(detections, x_offset=0, y_offset=0):
    formatted_detections = []
    for det in detections:
        detected_object = {
            "objectName": det[5],
            "confidence": float(det[4]),
            "x1": int(det[0] + x_offset),
            "y1": int(det[1] + y_offset),
            "x2": int(det[2] + x_offset),
            "y2": int(det[3] + y_offset)
        }
        formatted_detections.append(detected_object)
    return formatted_detections

# Function to display image with detections
def display_image_with_detections(frame, detections, window_name="Detections"):
    for det in detections:
        cv2.rectangle(frame, (det['x1'], det['y1']), (det['x2'], det['y2']), (0, 255, 0), 2)
        cv2.putText(frame, f"{det['objectName']} {det['confidence']:.2f}", (det['x1'], det['y1'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow(window_name, frame)

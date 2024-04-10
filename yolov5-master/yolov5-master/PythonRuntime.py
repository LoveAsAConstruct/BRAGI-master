from flask import Flask, jsonify
import cv2
import torch
import numpy as np

app = Flask(__name__)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Load homography matrix
homographyMatrix = np.load('homography_matrix.npy')


def apply_homography_to_bbox(x1, y1, x2, y2, H):
    """Apply homography to bounding box coordinates."""
    pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype='float32').reshape(-1, 1, 2)
    pts_transformed = cv2.perspectiveTransform(pts, H).reshape(-1, 2)
    x1_new, y1_new = np.min(pts_transformed, axis=0)
    x2_new, y2_new = np.max(pts_transformed, axis=0)
    return int(x1_new), int(y1_new), int(x2_new), int(y2_new)


def detect_objects_in_frame(frame):
    """Detect objects in a given frame."""
    cropped_frame = preprocess_frame(frame)
    detections = perform_detection(cropped_frame)
    processed_detections = process_detections(detections, frame.shape[:2], 0, frame.shape[0] - 345)
    return processed_detections


def preprocess_frame(frame, bgr_mode = False, width = 320, height = 344):
    """Preprocess frame for detection."""
    y = frame.shape[0] - height
    cropped_frame = frame[y:y+height, 0:width]
    return cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB if not bgr_mode else None)


def perform_detection(frame):
    """Perform object detection on the frame."""
    return model(frame).pandas().xyxy[0]


def process_detections(detections, frame_dimensions, x_offset, y_offset):
    """Process detections and apply homography."""
    detected_objects = []
    for _, row in detections.iterrows():
        x1, y1, x2, y2 = apply_homography_to_bbox(
            row['xmin'], row['ymin'], row['xmax'], row['ymax'], homographyMatrix)
        detected_objects.append({
            "objectName": row['name'],
            "confidence": float(row['confidence']),
            "x1": x1 + x_offset,
            "y1": y1 + y_offset,
            "x2": x2 + x_offset,
            "y2": y2 + y_offset
        })
    return detected_objects


@app.route('/detect', methods=['GET'])
def handle_detection_request():
    ret, frame = cap.read()
    if not ret:
        return jsonify({"error": "Failed to capture frame"})
    detections = detect_objects_in_frame(frame)
    return jsonify(detections)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

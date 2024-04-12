from flask import Flask, jsonify
import cv2
import torch
import numpy as np

app = Flask(__name__)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Load homography matrix
homographyMatrix = np.load('homography_matrix.npy')


def apply_homography_to_bbox(x1, y1, x2, y2, H = homographyMatrix):
    """Apply homography to bounding box coordinates."""
    pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype='float32').reshape(-1, 1, 2)
    pts_transformed = cv2.perspectiveTransform(pts, H).reshape(-1, 2)
    x1_new, y1_new = np.min(pts_transformed, axis=0)
    x2_new, y2_new = np.max(pts_transformed, axis=0)
    return int(x1_new), int(y1_new), int(x2_new), int(y2_new)
def apply_homography_to_image(image, H = homographyMatrix):
    height, width = image.shape[:2]
    transformed_image = cv2.warpPerspective(image, H, (width, height))
    return transformed_image
def image_preview(image, apply_homography=False):
    if apply_homography:
        updated_image = apply_homography_to_image(image)
    else:
        updated_image = image
    detections = detect_objects_in_frame(updated_image)
     # Optionally, draw bounding boxes on the transformed image
    updated_image = draw_detection_boxes_on_frame(updated_image, detections)
    return updated_image
def draw_detection_boxes_on_frame(image, detections):
    updated_image = image
    for det in detections:
        start_point = (det["x1"], det["y1"])
        end_point = (det["x2"], det["y2"])
        color = (255, 0, 0)  # Blue in BGR
        cv2.rectangle(updated_image, start_point, end_point, color, 2)
        label = f"{det['objectName']} {det['confidence']:.2f}"
        cv2.putText(updated_image, label, (det["x1"], det["y2"] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return updated_image

def detect_objects_in_frame(frame):
    """Detect objects in a given frame."""
    cropped_frame = preprocess_frame(frame)
    detections = perform_detection(cropped_frame)
    processed_detections = process_detections(detections, frame.shape[:2], 0, 0)
    return processed_detections


def preprocess_frame(frame, bgr_mode = False, width = 320, height = 344):
    """Preprocess frame for detection."""
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB if not bgr_mode else None)
    y = frame.shape[0] - height
    cropped_frame = frame[y:y+height, 0:width]
    return cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB if not bgr_mode else None)


def perform_detection(frame):
    """Perform object detection on the frame."""
    return model(frame).pandas().xyxy[0]


def process_detections(detections, frame_dimensions, x_offset, y_offset, apply_homography=False, H=None):
    """Process detections and optionally apply homography."""
    detected_objects = []
    for det in detections:  # Now directly iterating over the list of dictionaries
        # Extract coordinates directly without using DataFrame methods
        x1, y1, x2, y2 = det['xmin'], det['ymin'], det['xmax'], det['ymax']
        #if apply_homography and H is not None:
        #    x1, y1, x2, y2 = apply_homography_to_bbox(x1, y1, x2, y2, H)
        # Create the detection dictionary using the possibly transformed coordinates
        detected_object = {
            "objectName": det['name'],
            "confidence": float(det['confidence']),
            "x1": int(x1 + x_offset),
            "y1":int( y1 + y_offset),
            "x2": int(x2 + x_offset),
            "y2": int(y2 + y_offset)
        }
        detected_objects.append(detected_object)
    return detected_objects


def detect_objects_in_frame(frame, apply_homography = False):
    """Detect objects in a given frame."""
    cropped_frame = preprocess_frame(frame)
    detections_df = perform_detection(cropped_frame)  # Returns a DataFrame
    detections = detections_df.to_dict('records')  # Convert DataFrame to a list of dictionaries
    processed_detections = process_detections(detections, frame.shape[:2], 0, frame.shape[0] - 345, apply_homography, homographyMatrix)
    return processed_detections




@app.route('/detect', methods=['GET'])
def handle_detection_request():
    ret, frame = cap.read()
    if not ret:
        return jsonify({"error": "Failed to capture frame"})
    detections = detect_objects_in_frame(frame)
    return jsonify(detections)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

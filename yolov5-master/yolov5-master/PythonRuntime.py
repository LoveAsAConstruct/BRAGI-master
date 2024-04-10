import threading
from flask import Flask, jsonify
import cv2
import torch
import numpy as np
app = Flask(__name__)


class FrameStore:
    def __init__(self):
        self.frame = None
        self.lock = threading.Lock()

    def update(self, new_frame):
        with self.lock:
            self.frame = new_frame

    def get(self):
        with self.lock:
            return self.frame

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)

# Initialize video capture
cap = cv2.VideoCapture(0)
homographyMatrix = np.load('homography_matrix.npy')


def apply_homography_to_bbox(x1, y1, x2, y2, H):
    """Apply homography H to the bounding box coordinates."""
    # Corners of the original bounding box
    pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype='float32').reshape(-1, 1, 2)
    
    # Apply homography
    pts_transformed = cv2.perspectiveTransform(pts, H).reshape(-1, 2)
    
    # Calculate the axis-aligned bounding box of the transformed points
    x1_new, y1_new = np.min(pts_transformed, axis=0)
    x2_new, y2_new = np.max(pts_transformed, axis=0)
    
    return int(x1_new), int(y1_new), int(x2_new), int(y2_new)


frame_store = FrameStore()

def get_frame_and_detect():
    ret, frame = cap.read()
    if not ret:
        return {"error": "Failed to capture frame"}

    # Crop the image to the specified ROI
    # Assuming (0, 0) is the top-left corner of the image
    height, width = frame.shape[:2]  # Get the dimensions of the frame
    x = 0  # Bottom left corner X coordinate
    y = height - 345  # Bottom left corner Y coordinate (start from the bottom)
    cropped_frame = frame[y:y+344, x:x+320]

    # Convert cropped frame to RGB (required by YOLOv5) and run detection
    cropped_frame_rgb = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
    results = model(cropped_frame_rgb)

    # Parse results
    # Extract detections from the cropped frame
    detections = results.pandas().xyxy[0]
    detected_objects = []
    
    for index, row in detections.iterrows():
        # Apply homography to each bounding box (if you still need to apply it after cropping)
        # Note: You may need to adjust this part depending on whether you want to apply the homography
        # to the cropped image or the original image.
        x1, y1, x2, y2 = apply_homography_to_bbox(
            row['xmin'], row['ymin'], row['xmax'], row['ymax'], homographyMatrix)

        detected_objects.append({
            "objectName": row['name'],
            "confidence": float(row['confidence']),
            # Adjust bounding box coordinates to map back to the original frame's reference
            "x1": x1 + x,
            "y1": y1 + y,
            "x2": x2 + x,
            "y2": y2 + y
        })
    print(f"Detected {detected_objects}")
    # After detections, draw the bounding boxes and labels on the frame
    for obj in detected_objects:
        start_point = (obj["x1"], obj["y1"])  # Top left corner
        end_point = (obj["x2"], obj["y2"])    # Bottom right corner
        color = (255, 0, 0)  # Bounding box color (Blue in BGR)
        thickness = 2  # Bounding box thickness

        # Draw the bounding box
        cv2.rectangle(cropped_frame_rgb, start_point,
                      end_point, color, thickness)

        # Put the label below the bounding box
        label = f"{obj['objectName']} {obj['confidence']:.2f}"
        cv2.putText(cropped_frame_rgb, label, (obj["x1"], obj["y2"] + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display the frame
    # Update the shared frame with the processed one
    frame_store.update(cropped_frame_rgb)

    return detected_objects


def display_loop():
    cv2.namedWindow('YOLO Detection', cv2.WINDOW_NORMAL)
    while True:
        frame = frame_store.get()
        if frame is not None:
            # Convert back to BGR for display if the frame was converted to RGB earlier
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow('YOLO Detection', frame_bgr)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Break the loop if 'q' is pressed
            break
    cv2.destroyAllWindows()


# Start the display thread
display_thread = threading.Thread(target=display_loop)
display_thread.start()

@app.route('/detect', methods=['GET'])
def detect_objects():
    detections = get_frame_and_detect()
    return jsonify(detections)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

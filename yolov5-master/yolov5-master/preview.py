import cv2
from PythonRuntime import preprocess_frame, perform_detection, process_detections

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def detect_and_display():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Crop the frame and then perform detection on the cropped frame.
        processed_frame = preprocess_frame(frame)
        detections = perform_detection(processed_frame)  # Assuming detection now happens on cropped frame.
        
        # Assuming `process_detections` now correctly adjusts coordinates for the cropped frame.
        processed_detections = process_detections(detections, processed_frame.shape[:2], 0, 0)

        # Display processed detections
        for det in processed_detections:
            start_point = (det["x1"], det["y1"])
            end_point = (det["x2"], det["y2"])
            color = (255, 0, 0)  # Blue in BGR
            cv2.rectangle(processed_frame, start_point, end_point, color, 2)
            label = f"{det['objectName']} {det['confidence']:.2f}"
            cv2.putText(processed_frame, label, (det["x1"], det["y2"] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        cv2.namedWindow('YOLO Detection', cv2.WINDOW_NORMAL)
        cv2.imshow('YOLO Detection', processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def display():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        processed_frame = preprocess_frame(frame)

        cv2.imshow('YOLO Detection', processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    detect_and_display()

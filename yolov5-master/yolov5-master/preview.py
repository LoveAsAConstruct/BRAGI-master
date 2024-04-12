import cv2
from PythonRuntime import *

# Initialize video capture
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

def detect_and_display():
    homography = False
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        processed_frame = image_preview(frame,homography)
        """
        # Crop the frame and then perform detection on the cropped frame.
        processed_frame = frame#preprocess_frame(frame)
        #detections = perform_detection(processed_frame)  # Assuming detection now happens on cropped frame.
        
        # Assuming `process_detections` now correctly adjusts coordinates for the cropped frame.
        processed_detections = process_detections(detections, processed_frame.shape[:2], 0, 0)

        # Display processed detections
        # Inside your detect_and_display function, when setting start_point and end_point
        for det in processed_detections:
            start_point = (int(det["x1"]), int(det["y1"]))  # Ensure integer values
            end_point = (int(det["x2"]), int(det["y2"]))    # Ensure integer values

            color = (255, 0, 0)  # Blue in BGR
            thickness = 2

            # Now, this should work without raising an error
            cv2.rectangle(processed_frame, start_point, end_point, color, thickness)
        """
        cv2.namedWindow('YOLO Detection', cv2.WINDOW_NORMAL)
        cv2.imshow('YOLO Detection', processed_frame)
        if cv2.waitKey(1) &0xFF == ord('e'):
            homography = not homography
        if cv2.waitKey(1) & 0xFF == ord('q'):
            homography = True

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

from detection_module import (
    load_yolov5_model, detect_objects, format_detections, display_image_with_detections, 
    load_homography_matrix, apply_homography
)
import cv2
def main():
    model = load_yolov5_model()
    H = load_homography_matrix()
    cap = cv2.VideoCapture(1)

    show_transformed = False
    if not cap.isOpened():
        print("Error: Unable to open video source.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            # Detect objects and format detections
            raw_detections = detect_objects(model, frame)
            detections = format_detections(raw_detections)  # Ensure detections are properly formatted

            if show_transformed:
                transformed_frame, transformed_detections = apply_homography(H, frame, detections)
                display_image_with_detections(transformed_frame, transformed_detections)
            else:
                display_image_with_detections(frame, detections)

            key = cv2.waitKey(1)
            if key == 27:  # ESC key to exit
                break
            elif key == ord('e'):
                show_transformed = not show_transformed  # Toggle transformation view

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

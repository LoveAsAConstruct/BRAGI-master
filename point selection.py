import cv2
import numpy as np

# Global list to store points
points = []

def click_event(event, x, y, flags, param):
    """Callback function to capture click events."""
    if event == cv2.EVENT_LBUTTONDOWN:
        # Store the coordinates of the clicked point
        points.append((x, y))

        # Show the point on the image window with a small circle
        cv2.circle(img, (x, y), 3, (255, 0, 0), -1)
        cv2.imshow('image', img)

        # Optionally, print the coordinates to the console
        print(f"Point selected: ({x}, {y})")

# Load your image
img = cv2.imread(r"C:\Users\NuVu\Downloads\BRAGI-master\BRAGI-master\LensCorrectionImages\DistortedImage.png")
cv2.imshow('image', img)

# Bind the click event function to the OpenCV window
cv2.setMouseCallback('image', click_event)

# Wait until any key is pressed
cv2.waitKey(0)

# Close all OpenCV windows
cv2.destroyAllWindows()

# Now, `points` contains all the coordinates of the clicked points.
print("Selected points:", points)

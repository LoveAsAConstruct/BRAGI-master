
import cv2
import numpy as np

def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Transform the clicked point
        clicked_point = np.array([[[x, y]]], dtype=np.float32)
        transformed_point = cv2.perspectiveTransform(clicked_point, homographyMatrix)
        
        # Draw the original point on the distorted image
        cv2.circle(distortedImage, (x, y), 5, (255, 0, 0), -1)
        
        # Draw the transformed point on the undistorted image
        tx, ty = transformed_point.ravel()
        cv2.circle(undistortedImage, (int(tx), int(ty)), 5, (255, 0, 0), -1)
        
        # Update the images to show the points
        cv2.imshow("Distorted Image", distortedImage)
        cv2.imshow("Undistorted Image", undistortedImage)

# Load the images
distortedImagePath = r"LensCorrectionImages\Headset_square.png"
undistortedImagePath = r"LensCorrectionImages\Ugrid_square.png"
distortedImage = cv2.imread(distortedImagePath)
undistortedImage = cv2.imread(undistortedImagePath)

# Verify images loaded successfully
if distortedImage is None or undistortedImage is None:
    print("Error loading images. Please check the file paths.")
    exit()

# Define the source and destination points for homography calculation

srcPoints = np.array([(746, 628), (647, 362), (903, 264), (997, 528), (1075, 776), (838, 868), (598, 962), (495, 719), (389, 460), (1, 286), (273, 180), (540, 79), (460, 1271), (695, 1180), (926, 1091), (1161, 1008)], dtype=np.float32)
dstPoints = np.array([(560, 560), (561, 344), (762, 345), (764, 560), (764, 779), (560, 779), (359, 781), (359, 561), (359, 343), (157, 125), (359, 126), (561, 128), (157, 995), (359, 996), (560, 998), (764, 997)], dtype=np.float32)

# Compute the homography matrix
homographyMatrix, _ = cv2.findHomography(srcPoints, dstPoints)

# Assuming homographyMatrix is your computed homography matrix
np.save('homography_matrix.npy', homographyMatrix)

# Set up window and set mouse callback function
cv2.namedWindow("Distorted Image")
cv2.setMouseCallback("Distorted Image", draw_circle)

# Display the images
cv2.imshow("Distorted Image", distortedImage)
cv2.imshow("Undistorted Image", undistortedImage)

cv2.waitKey(0)
cv2.destroyAllWindows()

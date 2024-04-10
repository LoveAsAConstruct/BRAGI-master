
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
distortedImagePath = r"C:\Users\NuVu\Downloads\BRAGI-master\BRAGI-master\LensCorrectionImages\DistortedImage.png"
undistortedImagePath = r"C:\Users\NuVu\Downloads\BRAGI-master\BRAGI-master\LensCorrectionImages\original2.png"
distortedImage = cv2.imread(distortedImagePath)
undistortedImage = cv2.imread(undistortedImagePath)

# Verify images loaded successfully
if distortedImage is None or undistortedImage is None:
    print("Error loading images. Please check the file paths.")
    exit()

# Define the source and destination points for homography calculation

srcPoints = np.array([(176, 148), (154, 93), (208, 74), (231, 126), (253, 180), (197, 206), (144, 224), (121, 170), (102, 114), (87, 73), (139, 45), (190, 33), (232, 24), (256, 62), (280, 111), (296, 162), (305, 211), (266, 231), (216, 255), (167, 270), (120, 283), (95, 243), (74, 187), (60, 140), 51, 95), (48, 63), (82, 40), (126, 16), (172, 6), (213, 0), (245, 1), (271, 16), (293, 55), (311, 98), (317, 152), (316, 202), (317, 243), (309, 278), (277, 295), (240, 313), (199, 325), (142, 312), (107, 315), (86, 287), (62, 252), (46, 209), (26, 158), (18, 119), (19, 85)], dtype=np.float32)
dstPoints = np.array([(292, 289), (291, 223), (356, 226), (356, 290), (356, 353), (290, 354), (227, 355), (228, 290), (226, 226), (226, 159), (291, 160), (355, 160), (420, 160), (421, 225), (420, 290), (420, 354), (420, 419), (355, 419), (292, 419), (226, 419), (162, 418), (161, 354), (161, 290), (161, 226), (162, 161), (161, 96), (227, 95), (291, 96), (355, 95), (421, 96), (485, 96), (485, 160), (485, 226), (484, 290), (484, 354), (485, 419), (485, 484), (420, 484), (356, 484), (291, 484), (227, 483), (161, 484), (97, 484), (98, 420), (97, 354), (97, 289), (98, 225), (98, 161), (96, 96)], dtype=np.float32)

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

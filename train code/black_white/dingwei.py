import cv2
import numpy as np
from PIL import Image

# Load the bordered image
bordered_image_path = 'images/path_to_save_corners_detected_image.png'
bordered_image = Image.open(bordered_image_path)

# Convert PIL Image to NumPy array
bordered_image_np = np.array(bordered_image)

# Check if the image is already in grayscale
if len(bordered_image_np.shape) == 2 or bordered_image_np.shape[2] == 1:
    # If the image is already a grayscale image, no need to convert
    gray_image = bordered_image_np
else:
    # Otherwise, convert the image to grayscale
    gray_image = cv2.cvtColor(bordered_image_np, cv2.COLOR_BGR2GRAY)

# Detect corners using goodFeaturesToTrack
corners = cv2.goodFeaturesToTrack(gray_image, maxCorners=4, qualityLevel=0.01, minDistance=30)


# Draw the corners on the image
if corners is not None:
    corners = np.int0(corners)
    for corner in corners:
        print(corner)
        x, y = corner.ravel()
        cv2.circle(bordered_image_np, (x, y), 5, (255, 0, 0), -1)

# Convert back to PIL Image from NumPy array to save or display
corner_detected_image = Image.fromarray(bordered_image_np)

# Save the image with corners detected
corner_detected_image.save('images/corner_detected_image.png')

# The corners coordinates
corner_coords = corners.reshape(-1, 2)
print(corner_coords)

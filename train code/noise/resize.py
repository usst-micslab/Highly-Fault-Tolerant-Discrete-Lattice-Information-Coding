import cv2
import numpy as np
from matplotlib import pyplot as plt
size = 1
# Load the image from file
image_path = 'img_2.png'
# Let's attempt to load the image again and check if it's loaded correctly before proceeding
img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# Check if the image has been loaded properly
if img is None:
    raise ValueError("The image did not load properly. Please check the file path and the file itself.")
else:
    # Perform the perspective transformation and resizing if the image is loaded successfully

    # Calculate the transformation points
    rows, cols = img.shape[:2]
    src_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1], [cols - 1, rows - 1]])
    dest_points = np.float32(
        [[0, 0], [size / 5 * (cols - 1), 0], [0, size / 5 * (rows - 1)], [size / 5 * (cols - 1), size / 5 * (rows - 1)]])

    # Calculate the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_points, dest_points)

    # Apply the perspective transformation to reduce the size to 4/5
    reduced_img = cv2.warpPerspective(img, M, (int(size / 5 * cols), int(size / 5 * rows)))

    # Enlarge the image back to its original size
    enlarged_img = cv2.resize(reduced_img, (cols, rows), interpolation=cv2.INTER_LINEAR)

    # Save the resulting image to a new file
    result_path_corrected = f'transformed_image_corrected{size}.png'
    cv2.imwrite(result_path_corrected, enlarged_img)



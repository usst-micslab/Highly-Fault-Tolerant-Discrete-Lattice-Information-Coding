import cv2
import numpy as np
from matplotlib import pyplot as plt
# Load the image from file
image_path = 'img_2.png'
# Let's attempt to load the image again and check if it's loaded correctly before proceeding
img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
# Apply a black box of size 20x20 to the center of the image
def apply_black_box(image, box_size):
    # Calculate the position of the top-left corner of the black box
    center_x, center_y = image.shape[1] // 2, image.shape[0] // 2
    top_left_x, top_left_y = center_x - box_size // 2, center_y - box_size // 2

    # Create a copy of the image to not alter the original
    img_with_black_box = image.copy()

    # Set the pixels of the defined box to black
    img_with_black_box[top_left_y:top_left_y + box_size, top_left_x:top_left_x + box_size] = 0

    return img_with_black_box


box_size = 100  # Size of the black box
img_with_black_box = apply_black_box(img, box_size)

# Save the image with a black box
path_black_box = f'image_with_black_box{box_size}.png'
cv2.imwrite(path_black_box, img_with_black_box)

# Display the original and the image with a black box
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(img_with_black_box, cmap='gray')
plt.title(f'Image with Black Box {box_size}x{box_size}')
plt.axis('off')

plt.tight_layout()
plt.show()


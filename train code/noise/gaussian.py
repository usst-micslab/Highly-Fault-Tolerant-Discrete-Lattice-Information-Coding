import cv2
import numpy as np
from matplotlib import pyplot as plt
size = 5
# Load the image from file
image_path = 'img_2.png'

img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
gaussian_blur_img = cv2.GaussianBlur(img, (size,size), 0)

# Save the resulting image
gaussian_blur_path = f'gaussian_blur_image{size}.png'
cv2.imwrite(gaussian_blur_path, gaussian_blur_img)

# Display the original and Gaussian blurred image
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(gaussian_blur_img, cmap='gray')
plt.title('Gaussian Blurred Image')
plt.axis('off')

plt.tight_layout()
plt.show()

gaussian_blur_path
import cv2
import numpy as np
from matplotlib import pyplot as plt
# Load the image from file
image_path = 'img_2.png'
# Let's attempt to load the image again and check if it's loaded correctly before proceeding
img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
jpeg_quality = 80  # Quality for JPEG compression (0-100, lower means more compression and less quality)

# Save the image with JPEG compression
jpeg_compressed_path = f'jpeg_compressed_image{jpeg_quality}.jpg'  # JPEG compression requires .jpg or .jpeg extension
cv2.imwrite(jpeg_compressed_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])


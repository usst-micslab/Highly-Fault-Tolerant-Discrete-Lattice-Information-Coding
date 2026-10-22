import cv2

# Load your image
img = cv2.imread('img_2.png', cv2.IMREAD_GRAYSCALE)

# Define the border width
border_size = 50

# Apply the black border to the original image
img_with_border = img.copy()
img_with_border[:border_size, :] = 0  # Top border
img_with_border[-border_size:, :] = 0  # Bottom border
img_with_border[:, :border_size] = 0  # Left border
img_with_border[:, -border_size:] = 0  # Right border

# Save or display your image as needed
# cv2.imshow('Image with Black Border', img_with_border)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Save the image with the black border
cv2.imwrite(f'image_with_black_border{border_size}.png', img_with_border)

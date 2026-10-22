from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt

# Load the image
img_path = 'images/111_hidden.png'
image = Image.open(img_path)

width, height = image.size
coefficients = (1, 0, -0.001, 0, 1, -0.001, 0, 0)

# Apply perspective transformation
transformed_image = image.transform((width, height), Image.PERSPECTIVE, coefficients, Image.BICUBIC)

# Add border to the transformed image
border_size = 50
bordered_image = ImageOps.expand(transformed_image, border=border_size, fill='white')

# Save and show the new image
output_path = 'images/transformed_with_border.png'
bordered_image.save(output_path)

# Display the result
plt.imshow(bordered_image)
plt.axis('off') # Hide the axis
plt.show()





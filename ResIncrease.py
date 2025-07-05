import cv2

# Load image
image = cv2.imread('low_res_image.jpg')

# Define new dimensions (e.g., 2x upscale)
width = image.shape[1] * 2
height = image.shape[0] * 2
resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

# Save output
cv2.imwrite('upscaled_image.jpg', resized_image)

print("Image resolution increased successfully.")

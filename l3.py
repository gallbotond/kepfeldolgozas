import cv2
import numpy as np

# Load the input image
input_image = cv2.imread("./img/eper.jpg")
cv2.imshow('original', input_image)

# Define the mask values
mask_values = np.array([[0.11, -0.58, 0.19],
                        [-0.24, 0.91, 0.31],
                        [-0.18, 0.02, -0.22]])

mask = cv2.UMat(mask_values)

# Apply the mask to the image
masked_image = cv2.filter2D(input_image, -1, mask)

# Display the masked image
cv2.imshow("Masked", masked_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
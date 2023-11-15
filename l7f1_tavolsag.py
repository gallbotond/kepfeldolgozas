import cv2
import numpy as np

# Load image
input_image = cv2.imread("./img/amoba.png", cv2.IMREAD_GRAYSCALE)
original_image = input_image.copy()

# Display the grayscale intensity image
cv2.imshow("Intensity Image", input_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Perform distance transform
distance_transform = cv2.distanceTransform(input_image, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)

# Convert the 32-bit output to 8-bit depth image
distance_transform = distance_transform.astype(np.uint8)

# Create a circular structuring element of size 5x5
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Dilate the distance transform map in a loop
for i in range(5):
    dilated_image = cv2.dilate(distance_transform, kernel)
    distance_transform[input_image != 0] = dilated_image[input_image != 0]
    cv2.imshow("Distance Transform", distance_transform)
    cv2.waitKey(0)

# Copy the dilated image to the original distance transform map where the original map is not zero
distance_transform[input_image != 0] = dilated_image[input_image != 0]
# distance_transform[distance_transform != 0] = input_image[distance_transform != 0]

# dilated_image.copyTo(original_image)

cv2.imshow("Distance Transform", distance_transform)
cv2.imshow("Original Image", original_image)
cv2.imshow("Dilated Image", dilated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
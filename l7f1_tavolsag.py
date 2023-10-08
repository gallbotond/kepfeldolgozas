# import cv2
# import numpy as np

# # Load binary image
# img = cv2.imread("./img/amoba.png", cv2.IMREAD_GRAYSCALE)

# # Distance transform
# dist_transform = cv2.distanceTransform(img, cv2.DIST_L2, 5)

# # Convert to 8-bit depth
# dist_transform = cv2.convertScaleAbs(dist_transform)

# # Define structuring element
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# # Dilate distance transform and copy back to original image
# for i in range(10):
#     dilated = cv2.dilate(dist_transform, kernel)
#     dist_transform[dilated > dist_transform] = dilated[dilated > dist_transform]

# # Normalize distance transform to range [0, 255]
# dist_transform_norm = cv2.normalize(dist_transform, None, 0, 255, cv2.NORM_MINMAX)

# # Invert distance transform and apply color map
# dist_transform_norm_inv = cv2.bitwise_not(dist_transform_norm)
# dist_transform_color = cv2.applyColorMap(dist_transform_norm_inv, cv2.COLORMAP_JET)

# # Display result
# cv2.imshow("Amoeba diameter estimation", dist_transform_color)
# cv2.waitKey(0)

# cv2.destroyAllWindows()






import cv2
import numpy as np

# Load image
input_image = cv2.imread("./img/amoba.png", cv2.IMREAD_GRAYSCALE)

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

cv2.imshow("Distance Transform", distance_transform)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np

# Load image as grayscale
gray_image = cv2.imread("./img/kukac.png", cv2.IMREAD_GRAYSCALE)

# Display the grayscale image
cv2.imshow("Gray Image", gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Create a new image with increasing intensity from left to right
intensity_image = np.zeros_like(gray_image)
for x in range(intensity_image.shape[1]):
    intensity_image[:, x] = x * 256 // intensity_image.shape[1]

# Display the intensity image
cv2.imshow("Intensity Image", intensity_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Perform the tophat transformation on the image
tophat_image = cv2.addWeighted(intensity_image, 0.9, gray_image, 0.1, 0)

# Display the tophat image
cv2.imshow("Tophat Image", tophat_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Perform the blackhat transformation on the image
blackhat_image = cv2.addWeighted(intensity_image, 0.5, gray_image, -0.1, 25)

# Display the blackhat image
cv2.imshow("Blackhat Image", blackhat_image)
cv2.waitKey(0)

# Assuming imKi is a NumPy array representing an image
threshold_value = 10
max_value = 255
threshold_type = cv2.THRESH_BINARY
# _, output = cv2.threshold(tophat_image, threshold_value, max_value, threshold_type)

kernel_size = 11
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
gradient = cv2.morphologyEx(tophat_image, cv2.MORPH_TOPHAT, kernel)
_, output = cv2.threshold(gradient, threshold_value, max_value, threshold_type)


cv2.imshow("Thresholded tophat Image", output)
cv2.waitKey(0)

# _, output = cv2.threshold(blackhat_image, threshold_value, max_value, threshold_type)

gradient = cv2.morphologyEx(blackhat_image, cv2.MORPH_BLACKHAT, gradient)
_, output = cv2.threshold(gradient, threshold_value, max_value, threshold_type)

cv2.imshow("Thresholded blackhat Image 2", output)
cv2.waitKey(0)

cv2.destroyAllWindows()









# import cv2
# import numpy as np

# # Load grayscale image
# img = cv2.imread("./img/kukac.png", cv2.IMREAD_GRAYSCALE)

# # Create image with increasing intensity from left to right
# intensity = np.zeros_like(img)
# for x in range(img.shape[1]):
#     intensity[:, x] = x * 256 // img.shape[1]

# # Display result
# cv2.imshow("Intensity image", intensity)
# cv2.waitKey(0)

# # Create composite image with brighter bugs
# background = np.ones_like(img) * 255
# composite = cv2.addWeighted(intensity, 0.9, background, 0.1, 0)
# composite = cv2.addWeighted(composite, 1, img, 1, 0)

# # Display result
# cv2.imshow("Composite image with brighter bugs", composite)
# cv2.waitKey(0)

# # Apply tophat transformation with increasing kernel size
# kernel_size = 11
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
# for i in range(10):
#     tophat = cv2.morphologyEx(composite, cv2.MORPH_TOPHAT, kernel)
#     kernel_size += 2
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

#     # Display result
#     cv2.imshow("Tophat transformation with increasing kernel size", tophat)
#     cv2.waitKey(0)

# # Perform the tophat transformation on the intensity image
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
# tophat_image = cv2.morphologyEx(intensity, cv2.MORPH_TOPHAT, kernel)

# # Display the tophat image
# cv2.imshow("Tophat Image", tophat_image)
# cv2.waitKey(0)

# # Perform the blackhat transformation on the intensity image
# blackhat_image = cv2.morphologyEx(intensity, cv2.MORPH_BLACKHAT, kernel)

# # Display the blackhat image
# cv2.imshow("Blackhat Image", blackhat_image)
# cv2.waitKey(0)

# cv2.destroyAllWindows()
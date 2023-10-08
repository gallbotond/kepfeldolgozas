
import numpy as np

# Load image
input_image = cv2.imread("./img/kukac.png")

# Convert image to grayscale
gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

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
blackhat_image = cv2.addWeighted(intensity_image, 0.9, gray_image, -0.1, 25)

# Display the blackhat image
cv2.imshow("Blackhat Image", blackhat_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
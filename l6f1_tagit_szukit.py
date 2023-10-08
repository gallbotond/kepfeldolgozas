import cv2
import numpy as np

# Load binary image
img = cv2.imread("./img/pityoka.png", cv2.IMREAD_GRAYSCALE)

# Define structuring element
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# Apply erosion followed by dilation (x10)
for i in range(10):
    img = cv2.erode(img, kernel)

for i in range(10):
    img = cv2.dilate(img, kernel)

# Display result
cv2.imshow("Erosion followed by dilation", img)
cv2.waitKey(0)

# Apply dilation followed by erosion (x10)
for i in range(10):
    img = cv2.dilate(img, kernel)

for i in range(10):
    img = cv2.erode(img, kernel)

# Display result
cv2.imshow("Dilation followed by erosion", img)
cv2.waitKey(0)

cv2.destroyAllWindows()
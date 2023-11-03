import cv2
import numpy as np

# Load binary image
img = cv2.imread("./img/pityoka.png", cv2.IMREAD_GRAYSCALE)
cv2.imshow("Original", img)
img2 = img.copy()

# Define structuring element
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# Apply erosion followed by dilation (x10)
for i in range(10):
    img = cv2.erode(img, kernel)
    cv2.imshow("Erosion", img)
    cv2.waitKey(0)

for i in range(10):
    img = cv2.dilate(img, kernel)
    cv2.imshow("Dilation", img)
    cv2.waitKey(0)

# Display result
cv2.imshow("Erosion followed by dilation", img)
cv2.waitKey(0)

# Apply dilation followed by erosion (x10)
for i in range(10):
    img2 = cv2.dilate(img2, kernel)
    cv2.imshow("Dilation2", img2)
    cv2.waitKey(0)

for i in range(10):
    img2 = cv2.erode(img2, kernel)
    cv2.imshow("Erosion2", img2)
    cv2.waitKey(0)

# Display result
cv2.imshow("Dilation followed by erosion", img2)
cv2.waitKey(0)

cv2.destroyAllWindows()
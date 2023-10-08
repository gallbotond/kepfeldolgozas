import cv2
import numpy as np

# Load binary image
img = cv2.imread("./img/pityoka.png", cv2.IMREAD_GRAYSCALE)

# Define initial structuring element
kernel_size = 3
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
n = 3

# Apply erosion followed by dilation with increasing kernel size
for i in range(n):
    img = cv2.erode(img, kernel)
    kernel_size += 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

for i in range(n):
    img = cv2.dilate(img, kernel)
    kernel_size += 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

# Display result
cv2.imshow("Erosion followed by dilation with increasing kernel size", img)
cv2.waitKey(0)

# Apply dilation followed by erosion with increasing kernel size
for i in range(n):
    img = cv2.dilate(img, kernel)
    kernel_size += 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

for i in range(n):
    img = cv2.erode(img, kernel)
    kernel_size += 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

# Display result
cv2.imshow("Dilation followed by erosion with increasing kernel size", img)
cv2.waitKey(0)

cv2.destroyAllWindows()
import cv2
import numpy as np

# Load binary image
img = cv2.imread("./img/pityoka.png", cv2.IMREAD_GRAYSCALE)
cv2.imshow("Original", img)
img2 = img.copy()

# Define initial structuring element
kernel_size = 3
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
n = 5

# Apply erosion followed by dilation with increasing kernel size
for i in range(n):
    img = cv2.erode(img, kernel)
    cv2.imshow("Erosion", img)
    cv2.waitKey(0)
    kernel_size += 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

for i in range(n):
    img = cv2.dilate(img, kernel)
    cv2.imshow("Dilation", img)
    cv2.waitKey(0)
    kernel_size += 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

# Display result
cv2.imshow("Erosion followed by dilation with increasing kernel size", img)
cv2.waitKey(0)

# Apply dilation followed by erosion with increasing kernel size
for i in range(n):
    img2 = cv2.dilate(img2, kernel)
    cv2.imshow("Dilation2", img2)
    cv2.waitKey(0)
    kernel_size += 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

for i in range(n):
    img2 = cv2.erode(img2, kernel)
    cv2.imshow("Erosion2", img2)
    cv2.waitKey(0)
    kernel_size += 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

# Display result
cv2.imshow("Dilation followed by erosion with increasing kernel size", img2)
cv2.waitKey(0)

cv2.destroyAllWindows()
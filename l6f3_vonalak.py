
import cv2
import numpy as np
import random

# Load color image
img = cv2.imread("./img/bond.jpg")
cv2.imshow("Original image", img)

# Draw random black lines on the image
for i in range(100):
    x1, y1 = random.randint(0, img.shape[1]), random.randint(0, img.shape[0])
    x2, y2 = random.randint(0, img.shape[1]), random.randint(0, img.shape[0])
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 2)

cv2.imshow("Random black lines", img)

# Define initial structuring element
kernel_size = 3
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

# Apply dilation with increasing kernel size
for i in range(10):
    img = cv2.dilate(img, kernel)
    kernel_size += 2
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

cv2.imshow("Dilated image with increasing kernel size", img)

# Draw random white lines on the image
for i in range(100):
    x1, y1 = random.randint(0, img.shape[1]), random.randint(0, img.shape[0])
    x2, y2 = random.randint(0, img.shape[1]), random.randint(0, img.shape[0])
    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)

cv2.imshow("Random white lines", img)

# Define initial structuring element
kernel_size = 3
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

# Apply erosion with increasing kernel size
for i in range(10):
    img = cv2.erode(img, kernel)
    kernel_size += 2
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

# Display result
cv2.imshow("Eroded image with increasing kernel size", img)
cv2.waitKey(0)

cv2.destroyAllWindows()
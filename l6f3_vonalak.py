# import cv2
# import numpy as np

# def draw_lines(image, color, thickness):
#     height, width, _ = image.shape
#     diagonal_length = int(np.sqrt(height**2 + width**2))

#     for i in range(0, diagonal_length, 10):
#         cv2.line(image, (0, i), (width, i), color, thickness)

#     return image

# def dilate_image(image, kernel_size):
#     kernel = np.ones((kernel_size, kernel_size), np.uint8)
#     dilated_image = cv2.dilate(image, kernel, iterations=1)

#     return dilated_image

# def erode_image(image, kernel_size):
#     kernel = np.ones((kernel_size, kernel_size), np.uint8)
#     eroded_image = cv2.erode(image, kernel, iterations=1)

#     return eroded_image

# # Load color image
# input_image = cv2.imread("./img/bond.jpg")

# # Convert image to black lines
# black_lines = draw_lines(input_image.copy(), (0, 0, 0), 1)

# # Dilate the image with increasing kernel size
# dilated_image = black_lines.copy()
# for kernel_size in range(3, 21, 2):
#     dilated_image = dilate_image(dilated_image, kernel_size)

# # Convert image to white lines
# white_lines = draw_lines(input_image.copy(), (255, 255, 255), 1)

# # Erode the image with increasing kernel size
# eroded_image = white_lines.copy()
# for kernel_size in range(3, 21, 2):
#     eroded_image = erode_image(eroded_image, kernel_size)

# # Display the images
# cv2.imshow("Original Image", input_image)
# cv2.imshow("Black Lines", black_lines)
# cv2.imshow("Dilated Image", dilated_image)
# cv2.imshow("White Lines", white_lines)
# cv2.imshow("Eroded Image", eroded_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


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
import cv2
import numpy as np

# Load the image
img = cv2.imread("./img/2.jpg")

# Create a copy of the image to draw lines on
img_lines = img.copy()

# Draw lines with increasing thickness
for db in range(20):
    pt1 = (np.random.randint(0, img_lines.shape[1]), np.random.randint(0, img_lines.shape[0]))
    pt2 = (np.random.randint(0, img_lines.shape[1]), np.random.randint(0, img_lines.shape[0]))
    thickness = 1 + db % 2
    cv2.line(img_lines, pt1, pt2, (0, 0, 0), thickness)

    # Display the image with lines
    cv2.imshow("Image with Lines", img_lines)
    cv2.waitKey(0)


for db in range(20):
    # Apply median filtering with increasing neighborhood size
    neighborhood_size = 2 * db + 1
    img_lines = cv2.medianBlur(img_lines, neighborhood_size)

    # Display the filtered image
    cv2.imshow("Filtered Image", img_lines)
    cv2.waitKey(0)

cv2.destroyAllWindows()
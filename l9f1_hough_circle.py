import cv2
import numpy as np

# Read the image as a color image
image = cv2.imread("./img/hod.jpg", cv2.IMREAD_COLOR)

# Set the radius of the circle
R = 89

# Split the image into color channels
channels = cv2.split(image)

# Find the color channel with the strongest edges for the circles
strongest_channel = None
strongest_edges = 0
for channel in channels:
    edges = cv2.Canny(channel, 100, 200)
    num_edges = cv2.countNonZero(edges)
    if num_edges > strongest_edges:
        strongest_channel = channel
        strongest_edges = num_edges
        print("Strongest edges: ", strongest_edges)
        cv2.imshow("strongest channel", strongest_channel)
        cv2.waitKey(0)

# Create a black image with a white circle at the center
imP = cv2.circle(np.zeros_like(strongest_channel), (strongest_channel.shape[1] // 2, strongest_channel.shape[0] // 2), R, 255, -1)
cv2.imshow("imP", imP)
cv2.waitKey(0)

# Create an empty list to store the points on the circle
circPoint = []

# Iterate over the imP image and add the coordinates of non-black pixels to circPoint
for y in range(imP.shape[0]):
    for x in range(imP.shape[1]):
        if imP[y, x] != 0:
            circPoint.append((x - imP.shape[1] // 2, y - imP.shape[0] // 2))
            imP[y, x] = 0

print(len(circPoint), circPoint)

# Iterate over the original image and update the intensity of points around detected edges
for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        if strongest_channel[y, x] > 0:
            for i in range(len(circPoint)):
                px = x + circPoint[i][0]
                py = y + circPoint[i][1]
                if 0 <= px < image.shape[1] and 0 <= py < image.shape[0]:
                    image[py, px] += 1

# Find the brightest pixel in the black image
_, max_val, _, max_loc = cv2.minMaxLoc(imP)

# Draw a colored circle on the original image at the position of the brightest pixel
cv2.circle(image, max_loc, R, (0, 0, 255), 2)

# Darken the found position in the black image
cv2.circle(imP, max_loc, 20, 0, -1)

# Display the original image with the colored circle
cv2.imshow("Original Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np

# Read image
img = cv2.imread("./img/agy.bmp", cv2.IMREAD_GRAYSCALE)

# Constants
Ng = 256
c = 3
m = 1.5
mm = -1.0 / (m - 1.0)
eps = 0.00000001

# Arrays
u = np.zeros((c, Ng))
v = np.zeros(c)
d2 = np.zeros((c, Ng))
H = np.zeros(Ng)

# Compute histogram
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        H[img[y, x]] += 1

# Initialize class prototypes
for i in range(c):
    v[i] = 255.0 * (i + 1.0) / (2.0 * c)

# FCM algorithm
for cycle in range(20):
    # Compute partition matrix
    for l in range(Ng):
        for i in range(c):
            d2[i, l] = (l - v[i]) ** 2
        winner = 0
        for i in range(c):
            if d2[winner, l] > d2[i, l]:
                winner = i
        if d2[winner, l] < eps:
            for i in range(c):
                u[i, l] = 0.0
            u[winner, l] = 1.0
        else:
            sum = 0.0
            for i in range(c):
                u[i, l] = d2[i, l] ** mm
                sum += u[i, l]
            for i in range(c):
                u[i, l] /= sum

    # Compute class prototypes
    for i in range(c):
        sumUp = 0.0
        sumDn = 0.0
        for l in range(Ng):
            sumUp += H[l] * u[i, l] ** m * l
            sumDn += H[l] * u[i, l] ** m
        v[i] = sumUp / sumDn

# Compute lookup table
lut = np.zeros((1, 256), dtype=np.uint8)
for l in range(Ng):
    winner = 0
    for i in range(1, c):
        if u[i, l] > u[winner, l]:
            winner = i
    lut[0, l] = round(v[winner])

# Apply lookup table to image
result = cv2.LUT(img, lut)

# Display result
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Draw fuzzy membership functions
imF = np.zeros((400, 768, 3), dtype=np.uint8)
for i in range(c):
    for l in range(Ng):
        cv2.circle(imF, (1 + 3 * l, round(400.0 * (1.0 - u[i, l]))), 2,
                   (255 * (i == 0), 255 * (i == 1), 255 * (i == 2)), -1)
cv2.imshow("Membership Functions", imF)
cv2.waitKey(0)
cv2.destroyAllWindows()
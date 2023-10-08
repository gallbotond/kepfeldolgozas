import cv2
import numpy as np

lut = np.zeros((1, 256, 3), dtype=np.uint8)
brightness = 0
contrast = 2
gamma = 2

# Build lookup table
for i in range(256):
    norm_i = i / 255.0
    val = 255.0 * np.clip((contrast * np.power(norm_i, gamma) + brightness), 0, 1)
    lut[0, i, 0] = lut[0, i, 1] = lut[0, i, 2] = val

im = cv2.imread("./img/eper.jpg")
cv2.imshow("Original", im)

output = cv2.LUT(im, lut)
cv2.imshow("Output", output)

cv2.waitKey(0)
cv2.destroyAllWindows()
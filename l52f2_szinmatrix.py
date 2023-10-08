import cv2
import numpy as np

# Read input image and create output image
im = cv2.imread("./img/eper.jpg")
out = np.zeros_like(im)

# Initialize color matrix parameters
b = 0 # brightness
c = 2 # contrast
s = 2 # saturation
t = (1.0 - c) / 2.0
sr = (1 - s) * 0.3086
sg = (1 - s) * 0.6094
sb = (1 - s) * 0.0820
custom_matrix = np.array([
    [c * (sr + s), c * sr, c * sr, 0],
    [c * sg, c * (sg + s), c * sg, 0],
    [c * sb, c * sb, c * (sb + s), 0],
    [t + b, t + b, t + b, 1]
], dtype=np.float32)

# Convert input image to float32 with alpha channel
in_float = im.astype(np.float32) / 255.0
in_float = cv2.cvtColor(in_float, cv2.COLOR_BGR2BGRA)

# Apply color matrix transformation
out = in_float.reshape(im.shape[0] * im.shape[1], 4)
out = out.dot(np.float32(custom_matrix).T)
out_float = out.reshape(im.shape[0], im.shape[1], 4)

# Convert output image to 8-bit BGR format
cv2.imshow("out fl", out_float)
out = cv2.cvtColor(out_float, cv2.COLOR_BGRA2BGR)
cv2.imshow("out", out)
out = (out * 255).astype(np.uint8)

# Display result
cv2.imshow("Original", im)
cv2.imshow("Output", out)
cv2.waitKey(0)
cv2.destroyAllWindows()
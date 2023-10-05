import cv2
import numpy as np

# Create a black image
img = cv2.imread('./img/amoba.png')

# Display the initial image
cv2.imshow("Initial Image", img)
cv2.waitKey(0)

# Apply median filtering iteratively
for i in range(2000):
  # Apply median filter with a large neighborhood size
  img_filtered = cv2.medianBlur(img, 21)

  # Display the filtered image
  cv2.imshow("Filtered Image", img_filtered)
  cv2.waitKey(1)

  # Update the image for the next iteration
  img = img_filtered.copy()
  
  # cv2.waitKey(0)

cv2.destroyAllWindows()
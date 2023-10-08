import cv2
import numpy as np

# Betoltes
img = cv2.imread("./img/kina2.jpg")
img2 = img.copy()
img3 = img.copy()
img4 = img.copy()
cv2.imshow('original', img)

# Maszk
mask1 = np.array([[-1, 0, 1],
                  [-1, 0, 1],
                  [-1, 0, 1]])
mask2 = np.array([[1, 0, -1],
                  [1, 0, -1],
                  [1, 0, -1]])
mask3 = np.array([[-1, -1, -1],
                  [0, 0, 0],
                  [1, 1, 1]])
mask4 = np.array([[1, 1, 1],
                  [0, 0, 0],
                  [-1, -1, -1]])

def gradient_mask(img, mask):
  maskmat = cv2.UMat(mask)
  
  img = cv2.filter2D(img, -1, maskmat)
  
  cv2.imshow("Szurt", img)
  cv2.waitKey(0)
  
  return img

sum = cv2.add(
  cv2.add(gradient_mask(img, mask1), gradient_mask(img2, mask2)), 
  cv2.add(gradient_mask(img3, mask3), gradient_mask(img4, mask4))
  )

# Display the masked image
cv2.imshow("Sum", sum)
cv2.waitKey(0)

ret, thresholded = cv2.threshold(sum, 127, 255, cv2.THRESH_BINARY)

cv2.imshow("Threshold", thresholded)
cv2.waitKey(0)
def update_threshold(value):
    # Apply Canny edge detection with the updated threshold value
    edges = cv2.Canny(image, value, value * 2)

    # Display the edge image
    cv2.imshow("Edges", edges)

# Load the input image
image = sum

# Create a window to display the image and the trackbar
cv2.namedWindow("Edges")
cv2.resizeWindow("Edges", 600, 800)
cv2.createTrackbar("Threshold", "Edges", 0, 255, update_threshold)

# Initialize with default threshold value
update_threshold(0)

# Wait for key press to exit
cv2.waitKey(0)

cv2.destroyAllWindows()
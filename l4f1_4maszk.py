import cv2
import numpy as np

# Betoltes
img = cv2.imread("./img/eper.jpg")
img2 = img.copy()
img3 = img.copy()
img4 = img.copy()
# cv2.imshow('original', img)

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
  mask = cv2.UMat(mask1)

  # Szűrés végrehajtása és képek megjelenítése
  while True:
      # Szures
      img = cv2.filter2D(img, -1, mask)
      
      cv2.imshow("Szurt", img)
      key = cv2.waitKey(1)
      
      # Kilépés a ciklusból, ha a 'q' gombot lenyomjuk
      if key == ord("q"):
          break

# Display the masked image
cv2.imshow("Szurt", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
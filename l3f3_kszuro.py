import cv2
import numpy as np

# Betoltes
img = cv2.imread("./img/repulo.JPG")
# cv2.imshow('original', img)

# Maszk
def mask_gen(k):
  mask_values = np.array([[0, -k / 4, 0],
                        [-k / 4, 1 + k, -k / 4],
                        [0, -k / 4, 0]])
  
  return mask_values


k = 0
# Szűrés végrehajtása és képek megjelenítése
while True:
    cv2.imshow("Szurt", img)
    key = cv2.waitKey(0)
    
    # Kilépés a ciklusból, ha a 'q' gombot lenyomjuk
    if key == ord("q"):
        break
    
    mask = cv2.UMat(mask_gen(k))
    k += 1
    
    # Szures
    img = cv2.filter2D(img, -1, mask)

# Display the masked image
cv2.imshow("Szurt", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
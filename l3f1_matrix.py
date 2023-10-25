import cv2
import numpy as np

# Betoltes
img = cv2.imread("./img/eper.jpg")
# cv2.imshow('original', img)

# Maszk
mask_values = np.array([[0, 0, 0],
                        [0, 0, 1],
                        [0, 0, 0]])

mask = cv2.UMat(mask_values)


# Szűrés végrehajtása és képek megjelenítése
while True:
    cv2.imshow("Szurt", img)
    key = cv2.waitKey(0)
    
    # Kilépés a ciklusból, ha a 'q' gombot lenyomjuk
    if key == ord("q"):
        break
    
    # Szures
    img = cv2.filter2D(img, -1, mask)

# Display the masked image
cv2.imshow("Szurt", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
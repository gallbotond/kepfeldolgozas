import cv2
import numpy as np

# Függvény az eltolás szűréshez
def eltolas_szures(img, dx, dy):
    rows, cols = img.shape[:2]
    # M = np.float32([[1, 0, 0], [0, 1, dy]]) # lefele
    # M = np.float32([[1, 0, 0], [0, 1, -dy]]) # felfele
    # M = np.float32([[1, 0, dx], [0, 1, 0]]) # jobbra
    # M = np.float32([[1, 0, -dx], [0, 1, 0]]) # balra
    M = np.float32([[1, 0, -dx], [0, 1, -dy]]) # balra fel
    shifted_img = cv2.warpAffine(img, M, (cols, rows))
    return shifted_img

# Kép betöltése
img = cv2.imread("./img/eper.jpg")

# Szűrés végrehajtása és képek megjelenítése
while True:
    cv2.imshow("Shifted Image", img)
    key = cv2.waitKey(0)
    
    # Kilépés a ciklusból, ha a 'q' gombot lenyomjuk
    if key == ord("q"):
        break
    
    # Eltolás szűrés végrehajtása
    img = eltolas_szures(img, 1, 1)

cv2.destroyAllWindows()
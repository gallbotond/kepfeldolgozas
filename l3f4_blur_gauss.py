import cv2 

# Betoltes
img = cv2.imread("./img/eper.jpg")
img2 = img.copy()

cv2.imshow('original', img)

k = 0
l = 1
# Szűrés végrehajtása és képek megjelenítése
while True:
    cv2.imshow("blur", img)
    cv2.imshow("gauss", img2)
    key = cv2.waitKey(0)
    
    # Kilépés a ciklusból, ha a 'q' gombot lenyomjuk
    if key == ord("q"):
        break
      
    k += 1
    l += 2
    
    # Szures
    img = cv2.blur(img, (k, k))
    img2 = cv2.GaussianBlur(img2, (l, l), 1)

cv2.waitKey(0)
cv2.destroyAllWindows
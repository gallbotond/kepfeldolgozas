import cv2
import numpy as np

# 1. Olvassuk be a hod.jpg állományt színes képként.
img = cv2.imread('./img/hod.jpg', cv2.IMREAD_COLOR)

# 2. const int R = 89;
R = 89

# 3. Split-eljük a képet és megjelenítve nézzük meg melyik színcsatornán a legerősebbek a körök és a továbbiakban csak azon dolgozzunk.
b, g, r = cv2.split(img)
circles = cv2.HoughCircles(g, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
circles = np.uint16(np.around(circles))
strongest_channel = g

# 4. Lefuttatunk a Canny éldetektáló algoritmust.
strongest_channel = cv2.Canny(strongest_channel, 100, 200)

# 5. Hozzunk létre egy 1 színcsatornás fekete képet és a közepére rajzoljunk egy fehér R sugarú kört.(imP)
imP = np.zeros((img.shape[0], img.shape[1], 1), np.uint8)
cv2.circle(imP, (img.shape[1] // 2, img.shape[0] // 2), R, (255, 255, 255), -1)

# 6. Készítünk egy olyan táblázatot, amelyikben benne vannak egy körnek a pontjai. Azok a pontok, amelyek rajta vannak egy, a keresett sugárral megegyező méretű körön. Ez a tömb a circPoint.
circPoint = []
nrcPix = 0
for i in range(imP.shape[0]):
    for j in range(imP.shape[1]):
        if imP[i, j] != 0:
            circPoint.append((j - imP.shape[1] // 2, i - imP.shape[0] // 2))
            imP[i, j] = 0
            nrcPix += 1

# 7. Bejárjuk az imP képet és minden nem fekete képpontnak a koordinátáit (középponthoz viszonyított koordinátákat) felvesszük a táblázatba. Közben minden képpont feketévé válik az imP képen.
for i in range(strongest_channel.shape[0]):
    for j in range(strongest_channel.shape[1]):
        if strongest_channel[i, j] != 0:
            for k in range(nrcPix):
                x, y = circPoint[k]
                if i + y >= 0 and i + y < strongest_channel.shape[0] and j + x >= 0 and j + x < strongest_channel.shape[1]:
                    imP[i + y, j + x] += 1

# 9. Bejárjuk a circPoint tömböt i-vel ha a körnek az (x, y) középponthoz viszonyított i-edik körpontja rajta van a képen, akkor kiolvassuk annak a képpontnak az intenzitását az imP képről és eggyel nagyobb értéket visszaírunk.
for i in range(nrcPix):
    x, y = circPoint[i]
    if img.shape[0] // 2 + y >= 0 and img.shape[0] // 2 + y < img.shape[0] and img.shape[1] // 2 + x >= 0 and img.shape[1] // 2 + x < img.shape[1]:
        if imP[img.shape[0] // 2 + y, img.shape[1] // 2 + x] > 0:
            img[img.shape[0] // 2 + y, img.shape[1] // 2 + x] = (0, 0, 255)

# 11. Az eredeti képre egy élénk színnel rajzolunk egy pmax középpontú R sugarú kört
pmax = np.unravel_index(imP.argmax(), imP.shape)
cv2.circle(img, (pmax[1], pmax[0]), R, (0, 255, 0), 2)

# 12. Az imP-ben a megtalált pmax helyét kifeketítjük(legalább egy 20 pixel sugarú kör területén)
cv2.circle(imP, (pmax[1], pmax[0]), 20, (0, 0, 0), -1)

# 13. Megjelenítjük az eredményt
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

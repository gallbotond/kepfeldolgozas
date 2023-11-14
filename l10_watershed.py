import cv2
import numpy as np

# def # imDebug(img, name):
    # cv2.imshow(name, img)
    # cv2.waitKey(0)

def getGray(img, x, y):
    return img[y, x]

def setGray(img, x, y, value):
    img[y, x] = value

def getColor(img, x, y):
    # get the rgb value of a pixel
    b, g, r = img[y, x]
    return [r, g, b]

def setColor(img, x, y, value):
    img[y, x] = value


# Define constants
bits = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)
dx = np.array([1, 1, 0, -1, -1, -1, 0, 1], dtype=np.int32)
dy = np.array([0, -1, -1, -1, 0, 1, 1, 1], dtype=np.int32)

# Load the image and convert to grayscale
imColor = cv2.imread("./img/3.JPG", 1)
imO = cv2.cvtColor(imColor, cv2.COLOR_BGR2GRAY)
# cv2.imshow("imO", imO)
# cv2.waitKey(0)

# Create images for gradient, inward and outward flow directions, and segmentation
imG = imO.copy()
imE = imO.copy()
imKi = imO.copy()
imBe = imO.copy()
imSegm = imColor.copy()
imSegmMed = imColor.copy()
imMap = imO.copy()
imL = np.zeros_like(imColor, dtype=np.int16)
# imDebug(imL, "imL")

# Compute gradients
imColors = cv2.split(imColor)
imSum = np.zeros_like(imO, dtype=np.float32)

i=0
for im in imColors:
    imL = cv2.Sobel(im, cv2.CV_16S, 1, 0)
    # imDebug(imL, f"imL{i}")
    imE = cv2.convertScaleAbs(imL)
    # imDebug(imE, f"imE{i}")
    imL = cv2.Sobel(im, cv2.CV_16S, 0, 1)
    # imDebug(imL, f"imL{i}")
    imG = cv2.convertScaleAbs(imL)
    # imDebug(imG, f"imG{i}")
    imG = cv2.add(imE, imG)
    # imDebug(imG, f"imG{i}")
    imSum = cv2.addWeighted(imSum.astype(np.float32), 1, imG.astype(np.float32), 0.33333, 0)
    # imDebug(imSum, f"imSum{i}")
    i += 1


imG = imSum.copy()

# Preprocessing step - Gaussian smoothing
imG = cv2.GaussianBlur(imG, (9, 9), 0)
# imDebug(imG, "imG")

# Initialization
cv2.erode(imG, imE, cv2.getStructuringElement(cv2.          MORPH_RECT, (3, 3)))
# imDebug(imE, "imE")

imSegm.fill(50)
imSegmMed.fill(150)
imBe.fill(0)
imKi.fill(8)
imMap.fill(0)

# Step 1 - keressük meg és kezeljük le az összes képpontot, ahol a gradiens térkép lejtős
# Bejárjuk a képet (x,y)-nal
for x in range(imBe.shape[1]):
    for y in range(imBe.shape[0]):
        fp = getGray(imG, x, y)
        q = getGray(imE, x, y)
        # ahol az erodált gradiens kisebb a lokális gradiensnél, ott lejtős helyen vagyunk
        if q < fp:
            # megkeressük, hogy melyik irányba a legmeredekebb a lejtő
            for irany in range(8):
                # létezik-e a vizsgált koordinátájú szomszéd
                if x + dx[irany] >= 0 and x + dx[irany] < imBe.shape[1] and y + dy[irany] >= 0 and y + dy[irany] < imBe.shape[0]:
                    fpv = getGray(imG, x + dx[irany], y + dy[irany])
                    # ha az adott irany szerinti szomszéd gradiense annyi mint a minimum gradiens a szomszédságban...
                    if fpv == q:
                        #...akkor beállítjuk a kifelé folyást az adott szomszéd irányába
                        setGray(imKi, x, y, irany)
                        # bejelöljük, hogy az (x,y) képpontban megvan a kifelé folyás iránya
                        setGray(imMap, x, y, 255)
                        # kiolvassuk a befelé folyás bitjeit a szomszédban...
                        volt = getGray(imBe, x + dx[irany], y + dy[irany])
                        # megmódosítjuk ...
                        adunk = bits[irany]
                        lesz = volt | adunk
                        # és visszaírjuk
                        setGray(imBe, x + dx[irany], y + dy[irany], lesz)
                        break

# megmutatjuk egy ablakban a lekezelt képpontok térképét és várunk gombnyomásra
# cv2.imshow("Ablak", imMap)
# cv2.waitKey()
# Step 2 - fennsíkon levő pontok lekezelése a gradiens térképen
# Kell egy FIFO lista amire képpontokat fogunk elhelyeni
fifo = np.zeros((imBe.shape[0] * imBe.shape[1], 2), dtype=int)
nextIn = 0
nextOut = 0
# Bejárjuk a képet (x,y)-nal
for x in range(imBe.shape[1]):
    for y in range(imBe.shape[0]):
        # olyan képpontot keresünk, ahol már el van döntve a kifelé folyás iránya de van olyan szomszédja,
        # ahol még nincs eldöntve
        fp = getGray(imG, x, y)
        pout = getGray(imKi, x, y)
        if pout == 8:
            continue
        # találtunk egy olyan képpontot, ahol a kifelé folyás iránya már el van döntve ...
        added = 0
        # ... és vizsgáljuk annak a szomszédjait
        for irany in range(8):
            if x + dx[irany] >= 0 and x + dx[irany] < imBe.shape[1] and y + dy[irany] >= 0 and y + dy[irany] < imBe.shape[0]:
                fpv = getGray(imG, x + dx[irany], y + dy[irany])
                pvout = getGray(imKi, x + dx[irany], y + dy[irany])
                if fpv == fp and pvout == 8:
                    # ha ide jutunk, akkor találtunk olyan szomszédot, ahol még nincs eldöntve a kifelé folyás iránya
                    # az ilyen (x,y) képpontokat felvesszük a FIFO listára
                    if added == 0:
                        fifo[nextIn] = [x, y]
                        nextIn += 1
                    added += 1

while nextOut < nextIn:
    # kiveszünk egy képpontot a listáról
    p = fifo[nextOut]
    nextOut += 1
    fp = getGray(imG, p[0], p[1])
    # megkeressük az összes olyan szomszédját, ahol még nincs eldöntve a kifolyás iránya
    for irany in range(8):
        if p[0] + dx[irany] >= 0 and p[0] + dx[irany] < imBe.shape[1] and p[1] + dy[irany] >= 0 and p[1] + dy[irany] < imBe.shape[0]:
            fpv = getGray(imG, p[0] + dx[irany], p[1] + dy[irany])
            pvout = getGray(imKi, p[0] + dx[irany], p[1] + dy[irany])
            if fp == fpv and pvout == 8:
                # bejelöljük a kifelé folyás irányát a szomszédtól felénk
                setGray(imKi, p[0] + dx[irany], p[1] + dy[irany], (irany + 4) % 8)
                # bejelöljük, hogy a szomszéd képpontban megvan a kifelé folyás iránya
                setGray(imMap, p[0] + dx[irany], p[1] + dy[irany], 255)
                # bejelöljük a befelé folyás irányát
                setGray(imBe, p[0], p[1], bits[(irany + 4) % 8] | getGray(imBe, p[0], p[1]))
                # az újonnan bejelölt szomszéd felkerül a listára
                fifo[nextIn] = [p[0] + dx[irany], p[1] + dy[irany]]
                nextIn += 1

# megmutatjuk az ablakban a lekezelt képpontok térképét és várunk gombnyomásra
# cv2.imshow("Ablak", imMap)
# cv2.waitKey(0)
# Step 3 - megkeressük a völgyekhez tartozó képpontokat a gradiens térképen
# Keresünk olyan képpontot, amilyikből még nincs bejelölve a kifelé folyás iránya
# Az ilyen képpontot kinevezzük lokális minimumnak és megkeressük körülötte azon
# pontokat, amelyiknek még nincs kifelé folyása, ezekből mind a lokális minimum felé fog folyni a víz
# Szükségünk van egy veremre
stack = []
nrStack = 0
# Bejárjuk a képet (x,y)-nal
for x in range(imBe.shape[1]):
    for y in range(imBe.shape[0]):
        fp = getGray(imG, x, y)
        pout = getGray(imKi, x, y)
        # Amelyik képpontban már megvan a kifelé folyás iránya azzal nem kell foglalkozni
        if pout != 8:
            continue
        # pout egy lokális minimumnak lesz kinevezve
        # Megkeressük azokat a szomszédokat, amelyeknek még nincs meg a kifelé folyási irányuk
        for irany in range(8):
            if x + dx[irany] >= 0 and x + dx[irany] < imBe.shape[1] and y + dy[irany] >= 0 and y + dy[irany] < imBe.shape[0]:
                fpv = getGray(imG, x + dx[irany], y + dy[irany])
                pvout = getGray(imKi, x + dx[irany], y + dy[irany])
                if pvout == 8 and fp == fpv:
                    # itt találtunk olyan szomszédot
                    # bejelöljük a kifelé folyást a lokális minimum felé
                    setGray(imKi, x + dx[irany], y + dy[irany], (irany + 4) % 8)
                    setGray(imMap, x + dx[irany], y + dy[irany], 255)
                    setGray(imBe, x, y, bits[(irany + 4) % 8] | getGray(imBe, x, y))
                    # a szomszéd képpontot betesszük a verembe
                    stack.append([x + dx[irany], y + dy[irany]])
                    nrStack += 1
        # amíg ki nem ürül a verem
        # TODO debug
        while stack:
            # kiveszünk egy képpontot és megnézzük, hogy a szomszédai között van-e olyan, akinek nincs megjelölve a
            # kifelé folyás iránya
            pv = stack.pop()
            nrStack -= 1
            fpv = getGray(imG, pv[0], pv[1])
            pvout = getGray(imKi, pv[0], pv[1])
            for irany in range(8):
                if pv[0] + dx[irany] >= 0 and pv[0] + dx[irany] < imBe.shape[1] and pv[1] + dy[irany] >= 0 and pv[1] + dy[irany] < imBe.shape[0]:
                    # itt találtunk létező szomszédot
                    fpvv = getGray(imG, pv[0] + dx[irany], pv[1] + dy[irany])
                    pvvout = getGray(imKi, pv[0] + dx[irany], pv[1] + dy[irany])
                    if fpv == fpvv and pvvout == 8 and not (pv[0] + dx[irany] == x and pv[1] + dy[irany] == y):
                        # itt találtunk olyan szomszédot
                        # bejelöljük a kifelé folyást pout felé
                        setGray(imMap, pv[0] + dx[irany], pv[1] + dy[irany], 255)
                        setGray(imKi, pv[0] + dx[irany], pv[1] + dy[irany], (irany + 4) % 8)
                        setGray(imBe, pv[0], pv[1], bits[(irany + 4) % 8] | getGray(imBe, pv[0], pv[1]))
                        # a szomszéd képpontot betesszük a verembe
                        stack.append([pv[0] + dx[irany], pv[1] + dy[irany]])
# megmutatjuk az ablakban a lekezelt képpontok térképét és várunk gombnyomásra
# itt már csak izolált fekete képpontok lesznek a fehér képen, ezek a lokális minimumok
# cv2.imshow("Ablak", imMap)
# cv2.waitKey()

# Step 4
# feltérképezzük a vízgyűjtő medencéket a lokális minimumokból kiindulva a víz folyásával fordított irányba haladva
# minden vízgyűjtő medencében kiszámoljuk az átlagos és a medián színt
# mindkettőből generálunk egy-egy külön kimeneti szegmentált képet
# ez a puffer a medián számításához kell
medbuff = np.zeros((imBe.shape[0] * imBe.shape[1]), dtype=np.uint32)
label = 0
nextIn = 0
spotSum = np.zeros(3, dtype=np.int32)

# Bejárjuk a képet (x,y)-nal
for x in range(imBe.shape[1]):
    for y in range(imBe.shape[0]):
        # keresünk lokális mimimumot
        pout = getGray(imKi, x, y)
        if pout != 8:
            continue
        # találtunk lokális mimimumot, betesszük a verembe
        # stack[nrStack++] = Point(x, y)
        stack.append([x, y])
        for i in range(3):
            spotSum[i] = 0
        # amíg üres nem lesz a verem
        while stack:
            # Kiveszünk egy képpontot a veremből és megnézzük, honnan folyik felénk a víz
            # Ahonnan felénk folyik a víz, azt a képpontot felvesszük az aktuális régióba és
            # betesszük a verembe is.
            # pv = stack[--nrStack]
            pv.x, pv.y = stack.pop()
            fifo[nextIn] = pv
            nextIn += 1
            r, g, b = getColor(imColor, pv.x, pv.y)
            spotSum[0] += int(b)
            spotSum[1] += int(g)
            spotSum[2] += int(r)
            o = int(r) * 0x10000 + int(g) * 0x100 + int(b)
            o += round(float(r) * 0.299 + float(g) * 0.587 + float(b) * 0.114) * 0x1000000
            medbuff[nextIn - 1] = o
            # setGray(imLabel, pv.x, pv.y, label)
            pvin = getGray(imBe, pv.x, pv.y)
            for irany in range(8):
                if (bits[irany] & pvin) > 0:
                    # setGray(imLabel, pv.x + dx[(irany + 4) % 8], pv.y + dy[(irany + 4) % 8], label)
                    # stack[nrStack++] = Point(pv.x + dx[(irany + 4) % 8], pv.y + dy[(irany + 4) % 8])
                    stack.append([pv.x + dx[(irany + 4) % 8], pv.y + dy[(irany + 4) % 8]])
        # a label azt számolja, hogy hány régió van összesen a szegmentált képen
        label += 1
        if nextIn < 2:
            print(nextIn)
        for i in range(3):
            spotSum[i] = round(spotSum[i] / nextIn)
        # kiszámoljuk a medián színt a quicksort segítségével
        medbuff = np.sort(medbuff[:nextIn])
        medR = (medbuff[nextIn // 2] % 0x1000000) // 0x10000
        medG = (medbuff[nextIn // 2] % 0x10000) // 0x100
        medB = (medbuff[nextIn // 2] % 0x100)
        for i in range(nextIn):
            # if (getGray(imMask, fifo[i].x, fifo[i].y) > 128)
            # itt festjük ki a régiót az átlagos színnel
            setColor(imSegm, fifo[i].x, fifo[i].y, np.array([spotSum[2], spotSum[1], spotSum[0]], dtype=np.uint8))
            # itt festjük ki a régiót a medián színnel
            setColor(imSegmMed, fifo[i].x, fifo[i].y, np.array([medR, medG, medB], dtype=np.uint8))
        nextIn = 0

# memória felszabadítás
del fifo, stack, medbuff

# no more steps
print(f"\nRegions: {label}\n")

# megmutatjuk egy ablakban a medián színekkel készített képet
cv2.imshow("Median", imSegmMed)

# megmutatjuk egy masik ablakban az átlagos színekkel készített képet
cv2.imshow("Atlag", imSegm)

# cv2.waitKey()
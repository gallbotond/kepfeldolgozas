# import cv2
# import numpy as np

# def set_black(im, x, y):
#     im[y, x] = 0

# def set_gray(im, x, y, v):
#     im[y, x] = v

# def get_gray(im, x, y):
#     return im[y, x]

# def golay():
#     golay = np.array([
#         [0, 0, 0, -1, 1, -1, 1, 1, 1],
#         [-1, 0, 0, 1, 1, 0, -1, 1, -1],
#         [1, -1, 0, 1, 1, 0, 1, -1, 0],
#         [-1, 1, -1, 1, 1, 0, -1, 0, 0],
#         [1, 1, 1, -1, 1, -1, 0, 0, 0],
#         [-1, 1, -1, 0, 1, 1, 0, 0, -1],
#         [0, -1, 1, 0, 1, 1, 0, -1, 1],
#         [0, 0, -1, 0, 1, 1, -1, 1, -1]
#     ], dtype=np.int8)

#     imO = cv2.imread("./img/untitled.bmp", cv2.IMREAD_GRAYSCALE)
#     imP = imO.copy()
#     cv2.imshow("golay", imO)
#     cv2.waitKey()

#     while True:
#         count = 0

#         for l in range(8):
#             for x in range(1, imO.shape[1] - 1):
#                 for y in range(1, imO.shape[0] - 1):
#                     if imO[y, x] > 0:
#                         erase = True
#                         index = 9 * l

#                         for j in range(y - 1, y + 2):
#                             for i in range(x - 1, x + 2):
#                                 if index < golay.shape[1]:
#                                   if (golay[l, index] == 1 and imO[j, i] == 0 or
#                                     golay[l, index] == 0 and imO[j, i] > 0):
#                                     erase = False
#                                 index += 1

#                         if erase:
#                             set_black(imP, x, y)
#                             count += 1

#             imO = imP.copy()

#         cv2.imshow("Ablak", imP)
#         key = cv2.waitKey(100)

#         if count == 0 or key == ord('q'):
#             break

#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# golay()


import cv2
import numpy as np

def get_gray(image, x, y):
    return image[y, x]

def set_black(image, x, y):
    image[y, x] = 0

def golay(img):
    Golay = np.array([
        [0, 0, 0],
        [-1, 1, -1],
        [1, 1, 1],
        [-1, 0, 0],
        [1, 1, 0],
        [-1, 1, -1],
        [1, -1, 0],
        [1, 1, 0],
        [1, -1, 0],
        [-1, 1, -1],
        [1, 1, 0],
        [-1, 0, 0],
        [1, 1, 1],
        [-1, 1, -1],
        [0, 0, 0],
        [-1, 1, -1],
        [0, 1, 1],
        [0, 0, -1],
        [0, -1, 1],
        [0, 1, 1],
        [0, -1, 1],
        [0, 0, -1],
        [0, 1, 1],
        [-1, 1, -1]
    ])

    imO = img
    imP = imO.copy()
    cv2.imshow("golay", imO)
    cv2.waitKey()

    while True:
        count = 0
        for l in range(8):
            for x in range(1, imO.shape[1] - 1):
                for y in range(1, imO.shape[0] - 1):
                    if get_gray(imO, x, y) > 0:
                        erase = True
                        index = 9 * l
                        for j in range(y - 1, y + 2):
                            for i in range(x - 1, x + 2):
                                if index < Golay.shape[0]:
                                    if (Golay[index, 0] == 1 and get_gray(imO, i, j) == 0) or (Golay[index, 0] == 0 and get_gray(imO, i, j) > 0):
                                        erase = False
                                index += 1
                        if erase:
                            set_black(imP, x, y)
                            count += 1
        imO = imP.copy()
        cv2.imshow("Ablak", imP)
        cv2.waitKey(100)
        if count == 0:
            break

# Load image
img = cv2.imread("./img/untitled.bmp", cv2.IMREAD_GRAYSCALE)

# Define Golay alphabet L masks
L1 = np.array([[0, 0, 0], [-1, 1, -1], [1, 1, 1]], dtype=np.int8)
L2 = np.rot90(L1)
L3 = np.rot90(L2)
L4 = np.rot90(L3)
L5 = np.fliplr(L1)
L6 = np.rot90(L5)
L7 = np.rot90(L6)
L8 = np.rot90(L7)

# Define structuring element as a 3x3 square
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

for i in range(0, 100):
    # Perform hit-or-miss transform with Golay alphabet L masks
    hitmiss1 = cv2.morphologyEx(img, cv2.MORPH_HITMISS, L1, kernel)
    hitmiss2 = cv2.morphologyEx(img, cv2.MORPH_HITMISS, L2, kernel)
    hitmiss3 = cv2.morphologyEx(img, cv2.MORPH_HITMISS, L3, kernel)
    hitmiss4 = cv2.morphologyEx(img, cv2.MORPH_HITMISS, L4, kernel)
    hitmiss5 = cv2.morphologyEx(img, cv2.MORPH_HITMISS, L5, kernel)
    hitmiss6 = cv2.morphologyEx(img, cv2.MORPH_HITMISS, L6, kernel)
    hitmiss7 = cv2.morphologyEx(img, cv2.MORPH_HITMISS, L7, kernel)
    hitmiss8 = cv2.morphologyEx(img, cv2.MORPH_HITMISS, L8, kernel)

    # Combine hit-or-miss results
    hitmiss = cv2.bitwise_or(hitmiss1, hitmiss2)
    hitmiss = cv2.bitwise_or(hitmiss, hitmiss3)
    hitmiss = cv2.bitwise_or(hitmiss, hitmiss4)
    hitmiss = cv2.bitwise_or(hitmiss, hitmiss5)
    hitmiss = cv2.bitwise_or(hitmiss, hitmiss6)
    hitmiss = cv2.bitwise_or(hitmiss, hitmiss7)
    hitmiss = cv2.bitwise_or(hitmiss, hitmiss8)

    # Check if there are any hit points
    if np.sum(hitmiss) == 0:
        break

    # Remove hit points from original image
    img = cv2.bitwise_and(img, cv2.bitwise_not(hitmiss))

# Display result
cv2.imshow("Result", img)


cv2.waitKey(0)

golay(img)
cv2.waitKey(0)

cv2.destroyAllWindows()
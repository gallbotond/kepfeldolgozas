import cv2
import numpy as np
import matplotlib.pyplot as plt

def convert_to_YCrCb(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2YCrCb)

def convert_to_BGR(im):
    return cv2.cvtColor(im, cv2.COLOR_YCrCb2BGR)

def equalize_histogram(im):
    if im.shape[2] % 2 == 0:
        return

    if im.shape[2] == 3:
        im = convert_to_YCrCb(im)

    Ng = 256
    H = [0] * Ng

    for x in range(im.shape[1]):
        for y in range(im.shape[0]):
            H[im[y, x, 0]] += 1

    uj = [0] * Ng
    sum = 0

    for n in range(Ng):
        uj[n] = (sum + H[n] // 2) // (im.shape[0] * im.shape[1] // Ng)

        if uj[n] > Ng - 1:
            uj[n] = Ng - 1

        sum += H[n]

    for x in range(im.shape[1]):
        for y in range(im.shape[0]):
            im[y, x, 0] = uj[im[y, x, 0]]

    if im.shape[2] == 3:
        im = convert_to_BGR(im)

    return im

def show_image_and_histogram(im):
  plt.subplot(221)
  plt.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
  plt.subplot(222)
  plt.hist(im[:,:,0].ravel(),256,[0,256], color='b')
  plt.xlim([0, 256])
  plt.subplot(223)
  plt.hist(im[:,:,1].ravel(),256,[0,256], color='g')
  plt.xlim([0, 256])
  plt.subplot(224)
  plt.hist(im[:,:,2].ravel(),256,[0,256], color='r')
  plt.xlim([0, 256])
  plt.show()

def equalize_and_show_image(im):
    equalized_im = equalize_histogram(im)
    show_image_and_histogram(equalized_im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# img = cv2.imread('img/cheguevara.jpg')
# show_image_and_histogram(img)

# equalize_and_show_image(img)
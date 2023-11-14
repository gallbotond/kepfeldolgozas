import cv2
import numpy as np

cap = cv2.VideoCapture('./vid/IMG_6909.MOV')
cap2 = cap

if not cap.isOpened():
    print("Cannot open file")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # rescale the frame
    f = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)

    # blur = 5

    # # use the median blur to reduce noise
    # f = cv2.medianBlur(f, blur)

    # # use gaussian blur to reduce noise
    # f = cv2.GaussianBlur(f, (blur, blur), 0)

    # use laplace high pass filter to reduce noise
    f = cv2.Laplacian(f, cv2.CV_64F)

    # detect the edges on the frame
    f_gray = cv2.cvtColor(f.astype(np.uint8), cv2.COLOR_BGR2GRAY)  # convert to grayscale
    f_gray = cv2.GaussianBlur(f_gray, (5, 5), 0)  # apply Gaussian blur
    f = cv2.Canny(f_gray, 100, 200)  # apply Canny edge detection

    cv2.imshow('frame', f)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
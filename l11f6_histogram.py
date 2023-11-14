import cv2
import numpy as np
from l5f1_hisztogram import equalize_histogram

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
    original = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)

    f2 = equalize_histogram(original)

    cv2.imshow('frame2', f2)
    cv2.imshow('original', original)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
import cv2
import numpy as np

def regionGrowing(im, p0, pbf, pja):
    count = 0
    fifo = np.zeros((0x100000, 2), dtype=int)
    nextIn = 0
    nextOut = 0
    pbf = p0
    pja = p0
    if im[p0[1], p0[0]] < 128:
        return 0
    fifo[nextIn] = p0
    nextIn += 1
    im[p0[1], p0[0]] = 100
    while nextIn > nextOut:
        p = fifo[nextOut]
        nextOut += 1
        count += 1
        if p[0] > 0:
            if im[p[1], p[0]-1] > 128:
                fifo[nextIn] = [p[0]-1, p[1]]
                nextIn += 1
                im[p[1], p[0]-1] = 100
                if pbf[0] > p[0]-1:
                    pbf = list(pbf)
                    pbf[0] = p[0]-1
                    pbf = tuple(pbf)
        if p[0] < im.shape[1]-1:
            if im[p[1], p[0]+1] > 128:
                fifo[nextIn] = [p[0]+1, p[1]]
                nextIn += 1
                im[p[1], p[0]+1] = 100
                if pja[0] < p[0]+1:
                    pja = list(pja)
                    pja[0] = p[0]+1
                    pja = tuple(pja)
        if p[1] > 0:
            if im[p[1]-1, p[0]] > 128:
                fifo[nextIn] = [p[0], p[1]-1]
                nextIn += 1
                im[p[1]-1, p[0]] = 100
                if pbf[1] > p[1]-1:
                    if pbf[1] > p[1]-1:
                        pbf = list(pbf)
                        pbf[1] = p[1]-1
                        pbf = tuple(pbf)
        if p[1] < im.shape[0]-1:
            if im[p[1]+1, p[0]] > 128:
                fifo[nextIn] = [p[0], p[1]+1]
                nextIn += 1
                im[p[1]+1, p[0]] = 100
                if pja[1] < p[1]+1:
                    pja = list(pja)
                    pja[1] = p[1]+1
                    pja = tuple(pja)
    return count

# read the video file
cap = cv2.VideoCapture('./vid/IMG_6909.MOV')

# check if the video file was successfully opened
if not cap.isOpened():
    print("Error opening video file")
    exit()

# read the first 10 frames and use the 5th frame as the background
for i in range(10):
    ret, frame = cap.read()
    if not ret:
        print("Error reading video file")
        exit()
    if i == 4:
        bg_frame = frame

# resize the background frame to a quarter of its original size
bg_frame = cv2.resize(bg_frame, (0, 0), fx=0.25, fy=0.25)

# convert the background frame to grayscale
bg_gray = cv2.cvtColor(bg_frame, cv2.COLOR_BGR2GRAY)

# loop through the remaining frames of the video
while True:
    # read a frame from the video file
    ret, frame = cap.read()

    # check if the frame was successfully read
    if not ret:
        break

    # resize the frame to a quarter of its original size
    frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate the absolute difference between the background and current frame
    diff = cv2.absdiff(bg_gray, gray)

    # threshold the difference image
    thresh = cv2.threshold(diff, 170, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes
    kernel = np.ones((3, 3), np.uint8)
    eroded = cv2.erode(thresh, kernel, iterations=2)

    im = eroded.copy()
    cv2.imshow('eroded', im)

    pbf = [0, 0]
    pja = [0, 0]
    roiSize = 0
    for y in range(im.shape[0]):
        for x in range(im.shape[1]):
            if im[y, x] > 128:
                res = regionGrowing(im, (x, y), pbf, pja)
                print(res)
                if res > 500 and res > roiSize:
                    roi = (pbf[0], pbf[1], pja[0] - pbf[0] + 1, pja[1] - pbf[1] + 1)
                    roiSize = res
                    print(roi)
    nrRect = roiSize // 500 if roiSize > 500 else 0

    if nrRect > 0:
        cv2.rectangle(frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 255, 255), 2)

    # # find contours in the dilated image
    # contours, hierarchy = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # # loop through the contours and draw bounding boxes around them
    # for contour in contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # display the resulting frame
    cv2.imshow('frame', frame)

    # wait for the user to press a key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the video file and close all windows
cap.release()
cv2.destroyAllWindows()
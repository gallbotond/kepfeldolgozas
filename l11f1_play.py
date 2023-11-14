import cv2

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
    # convert to grayscale
    f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', f)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
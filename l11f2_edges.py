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
    
    # detect the edges on the frame
    f = cv2.Canny(f, 100, 200)

    cv2.imshow('frame', f)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break

#     # rescale the frame
#     frame_rs = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
#     cv2.imshow('frame', frame_rs)

#     if cv2.waitKey(1) == ord('q'):
#         break
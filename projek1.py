import cv2
import numpy as np

cap = cv2.VideoCapture("resources/source-video-1.mp4")
def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("Hue Min", "HSV", 36, 179, empty)
cv2.createTrackbar("Hue Max", "HSV", 107, 179, empty)
cv2.createTrackbar("Sat Min", "HSV", 55, 255, empty)
cv2.createTrackbar("Sat Max", "HSV", 155, 255, empty)
cv2.createTrackbar("Val Min", "HSV", 51, 255, empty)
cv2.createTrackbar("Val Max", "HSV", 255, 255, empty)


while True:
    success, video = cap.read()
    if not success:
        break

    video = cv2.resize(video,(1600,800))

    videoHSV = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min", "HSV")
    h_max = cv2.getTrackbarPos("Hue Max", "HSV")
    s_min = cv2.getTrackbarPos("Sat Min", "HSV")
    s_max = cv2.getTrackbarPos("Sat Max", "HSV")
    v_min = cv2.getTrackbarPos("Val Min", "HSV")
    v_max = cv2.getTrackbarPos("Val Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # Buat mask untuk objek dalam lapangan
    mask = cv2.inRange(videoHSV, lower, upper)

    # Temukan kontur objek dalam lapangan
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Buat mask kosong untuk menggambar kontur
    contour_mask = np.zeros_like(mask)

    # Gambar kontur pada mask kosong
    cv2.drawContours(contour_mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # Gabungkan mask lapangan dengan mask kontur
    result = cv2.bitwise_and(video, video, mask=contour_mask)

    cv2.imshow("Result", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2

class Display():
    def __init__(self) -> None:
        pass

    def DisplayFrame(self, frame, keypoint):
        y, x, _ = frame.shape
        for k in keypoint[0,0,:,:]:
            if k[2] > 0.3:
                yc = int(k[0] * y)
                xc = int(k[1] * x)
                img = cv2.circle(frame, (xc, yc), 2, (0, 255, 0), 5)
                _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return buffer.tobytes()


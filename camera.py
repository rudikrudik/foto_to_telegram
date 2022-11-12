import cv2
import time


def screen_shot(number: int, cam: str):

    camera = cv2.VideoCapture(cam)
    codec = 0x47504A4D  # MJPG

    if not camera.isOpened():
        raise IOError("Не удается открыть камеру")

    camera.set(cv2.CAP_PROP_FPS, 30.0)
    camera.set(cv2.CAP_PROP_FOURCC, codec)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    for i in range(100):
        camera.read()

    return_value, image = camera.read()
    cv2.imwrite(f'cam{number}.jpg', image)
    camera.release()
    cv2.destroyAllWindows()
    time.sleep(2)

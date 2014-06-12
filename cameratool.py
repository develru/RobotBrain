__author__ = 'develru'

import cv2


class Capture:

    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def show_image(self):
        ret, frame = self.camera.read()
        cv2.imwrite('frame.png', frame)
        # cv2.imshow('frame', frame)
        # cv2.waitKey(0)

    def close(self):
        self.camera.release()
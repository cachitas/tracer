import cv2


class Video:

    def __init__(self, filename):
        self.filename = filename
        self.capture = cv2.VideoCapture(filename)

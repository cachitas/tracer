import os
import cv2


class Video:

    def __init__(self, filename):
        self.filename = filename
        self.capture = cv2.VideoCapture(filename)

    def read(self):
        """Read frame."""
        success, image = self.capture.read()
        if success:
            return image
        else:
            raise Exception("Failed to read frame")


video = Video('sample_videos/single.avi')

img = video.read()
print(img)
cv2.imshow('da', img)
cv2.waitKey()





import os
import cv2
import ocvu
import imageio
from joblib import Parallel, delayed
import matplotlib.pylab as pl
import numpy as np
import pandas as pd
from skimage import color
from skimage import feature
from skimage import filters
from skimage import io
from skimage import measure
from skimage import util
# from skimage import viewer  # requires Qt
from tqdm import tqdm


def imshow(image, title=""):
    pl.figure()
    pl.title(title)
    pl.imshow(image)
    pl.show()


# Global parameters
# -----------------

N = 2  # number of flies expected

# Load video into memory
filename = os.path.join('sample_videos', 'couple.avi')
print(filename)
video_reader = imageio.get_reader(uri=filename, format='FFMPEG')
video_len = len(video_reader)

print(video_reader, video_len)

nblobs = []
for index, image in enumerate(tqdm(video_reader)):

    # cv2.imshow('image', image)
    # image = color.rgb2gray(image)
    # image = 1 - image  # replaces `invert` above

    image = image[:, :, 1]
    _, fg_mask = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY_INV)
    print(fg_mask)
    imshow(fg_mask)

    # blobs = feature.blob_dog(image, max_sigma=30)
    blobs = ocvu.find_biggest_contours(fg_mask, 10)
    print(blobs)
    for blob in blobs:
        print(blob.centroid, blob.area)
    break

    if len(blobs) == N:
        nblobs.append(index)
    if len(nblobs) >= 100:
        break

del video_reader

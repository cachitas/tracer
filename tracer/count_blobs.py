import os
import cv2
import ocvu
import imageio
import pandas as pd
from tqdm import tqdm


# Load video into memory
filename = os.path.join('sample_videos', 'couple.avi')
video_reader = imageio.get_reader(uri=filename, format='FFMPEG')
video_len = len(video_reader)


# Select 300 frames with n connected components
area_min = 2000
area_max = 3000
s = pd.Series(index=range(len(video_reader)))
for index, image in enumerate(tqdm(video_reader)):
    image = image[:, :, 1]
    _, fg_mask = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
    blobs = ocvu.find_biggest_contours(fg_mask, 10)
    blobs = [blob for blob in blobs if area_min < blob.area < area_max]
    s.loc[index] = len(blobs)

s.to_csv('nblobs.csv')

# Terminate
video_reader.close()

import os
import cv2
import ocvu
import imageio
import pandas as pd
from skimage import color
from tqdm import tqdm


# Load video into memory
filename = os.path.join('sample_videos', 'couple.avi')
video_reader = imageio.get_reader(uri=filename, format='FFMPEG')
video_len = len(video_reader)


# Select 300 frames with n connected components
area_min = 1500
area_max = 3000
df = pd.DataFrame(index=range(len(video_reader)), columns=['nblobs', 'areas'])
for index, image in enumerate(tqdm(video_reader)):
    image = image[:, :, 1]
    # _, fg_mask = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
    # blobs = ocvu.find_biggest_contours(fg_mask, n=10, area_min=area_min)
    # blobs = [blob for blob in blobs if area_min < blob.area < area_max]

    # image = color.rgb2gray(image)
    # _, fg_mask = cv2.threshold(image, .8, 1.0, cv2.THRESH_BINARY_INV)
    # blobs = ocvu.find_biggest_contours(fg_mask, n=10, area_min=area_min)

    # df.loc[index, 'nblobs'] = len(blobs)
    # for i, blob in enumerate(blobs):
    #     df.loc[index, 'area%d' % i] = blob.area

df.to_csv('nblobs.csv')

# Terminate
video_reader.close()

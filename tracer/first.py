import os
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


# Global parameters
# -----------------

N = 2  # number of flies expected

# Load video into memory
filename = os.path.join('sample_videos', 'couple.avi')
print(filename)
video_reader = imageio.get_reader(uri=filename, format='FFMPEG')
video_len = len(video_reader)

print(video_reader, video_len)

# video = np.zeros(shape=(video_len, 1024, 1024), dtype=np.uint8)
# for i, image in enumerate(video_reader):
#     image = image[:, :, 1]
#     video[i] = image
# print(len(video), video)


# Select 100 frames with n connected components
df = pd.DataFrame(index=range(len(video_reader)))


def count_blobs(image):
    image = color.rgb2gray(image)
    image = 1 - image  # replaces `invert` above
    blobs = feature.blob_dog(image, max_sigma=30)
    return len(blobs)


Parallel(n_jobs=8, verbose=1, backend='threading')(
    delayed(count_blobs)(image) for image in video_reader)

print(df)

# nblobs = []
# for index, image in enumerate(tqdm(video_reader)):
#     image = color.rgb2gray(image)
#     image = 1 - image  # replaces `invert` above
#     blobs = feature.blob_dog(image, max_sigma=30)

#     if len(blobs) == N:
#         nblobs.append(index)
#     if len(nblobs) >= 100:
#         break
#     # fig, axs = pl.subplots(ncols=3)
#     # axs[0].imshow(image, cmap='gray')
#     # # axs[1].imshow(mask, cmap='gray')

#     # axs[2].set_aspect('equal')
#     # axs[2].set_xlim(0, 1024)
#     # axs[2].set_ylim(-1024, 0)
#     # for blob in blobs:
#     #     y, x, s = blob
#     #     print(x, y, s)
#     #     axs[2].scatter(x, -y, s*np.sqrt(2))

#     # pl.show()
#     # break

# print(nblobs)
# pl.plot(nblobs)
# pl.show()

del video_reader

import os

import numpy as np
import pandas as pd
import pylab as pl

import tracer


if __name__ == '__main__':
    filename = os.path.join('sample_videos', 'single.avi')
    # video, fps = tracer.load_video(filename)
    # print(video.shape)
    # print(video[-1])

    # np.save(filename[:-4], video, allow_pickle=False, fix_imports=False)

    print("Loading saved video")
    video = np.load(filename[:-4] + '.npy')
    print(video.shape)
    print(video[-1])

    # df = pd.read_csv('nblobs.csv', index_col=0)
    # print(df.head())
    # df[df.nblobs == 2].area0.hist(histtype='step')
    # df[df.nblobs == 2].area1.hist(histtype='step')
    # pl.show()
    # print(df[df.nblobs == 1].describe())

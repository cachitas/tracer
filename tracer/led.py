"""
This is a quick way of detecting an LED in the top right corner.
"""

import argparse
import multiprocessing as mp

import pylab as pl
import pandas as pd

from . import tools
from .io.video import Video

ROI_SIZE = 250


def compute_roi_mean_intensity(video, indexes):
    s = pd.Series(0.0, index=indexes)
    for image in video.get_chunk(indexes):
        index = image.meta.index
        image = image[-ROI_SIZE:, :ROI_SIZE]
        s.loc[index] = image.mean()
    return s


parser = argparse.ArgumentParser(description='LED')
parser.add_argument('video_filepath', type=str,
                    help='video file path')
# parser.add_argument('-s', '--size', type=int, default=250,
#                     help='')
args = parser.parse_args()

video = Video(args.video_filepath)

print(video.filepath, video.nframes, video.fps)

tasks = [
    (
        video,
        chunk,
    )
    for chunk in tools.split_in_chunks(video.frames, 8)
]
processes = min(len(tasks), mp.cpu_count())
with mp.Pool(processes) as pool:
    intensities = pool.starmap(compute_roi_mean_intensity, tasks)
intensities = pd.concat(intensities)

diff = intensities.diff()

led_on = diff[diff > 1].index
led_off = diff[diff < -1].index

# print(led_on)
# print(led_off)

# intensities.plot()
# diff.plot(secondary_y=True)
# pl.show()

assert len(led_on) == len(led_off)

times = [(on, off) for on, off in zip(led_on, led_off)]

print("Found %d LED blinks" % len(times))

for i, (on, off) in enumerate(times):
    print("Blink %2d lasts %3.1f seconds" % (i+1, (off-on)/video.fps))

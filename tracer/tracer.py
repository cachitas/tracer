import logging
import os

import imageio
import numpy as np
from tqdm import tqdm, trange

# from tools import LoggingHandler


log = logging.getLogger(__name__)
# log.addHandler(LoggingHandler())

video = None
output_folder = None
background_model = None


class Video:

    def __init__(self, filepath):
        self.filepath = filepath
        self.reader = imageio.get_reader(filepath, format='FFMPEG', mode='I')
        self.metadata = self.reader.get_meta_data()

    @property
    def fps(self):
        """Returns the frame rate as a float"""
        return self.metadata['fps']

    @property
    def nframes(self):
        """Returns the number of frames as an int"""
        return self.metadata['nframes']

    @property
    def size(self):
        """Returns a tuple with (width, height)."""
        return self.metadata['size']

    def close(self):
        """Close the reader object."""
        self.reader.close()

    def read(self, index):
        """Read a video frame in grayscale.
        The frame number is stored in the `.meta.index` attribute (imageio).
        """
        image = self.frames[index]
        if np.count_nonzero(image) == 0:
            image = self.reader.get_data(index)
            image = image[:, :, 1]
            image.meta.index = index
        return image


def _mean_squared_error(img1, img2):
    """
    The **Mean Squared Error** between the two images is the sum of the
    squared difference between the two images. The lower the error, the
    more *similar* the two images are.
    **NOTE:** the two images must have the same dimension.
    """
    err = np.sum((img1.astype('float') - img2.astype('float')) ** 2)
    err /= float(img1.shape[0] * img1.shape[1])
    return err


def generate_background_model(step=None, end=None, mse_min=50):
    """Generates a background model using the median.
    Only sufficiently different frames are considered, using the
    mean squared error method.
    Parameters:
        step: Step to iterate through the video. Default is video FPS rate.
        end: Last frame to consider. Default is 2/3 of video length.
        mse_min: The minimum error at wich the frame is selected. The
            lower the error, the more *similar* the two images are.
    """
    log.info("Generating background model")

    step = step or int(video.fps)
    end = end or int(video.nframes * (2 / 3))

    log.info(
        "Selecting frames (step={}, end={}, mse_min={})".format(
            step, end, mse_min)
    )

    first_frame = video.read(0)
    selected_frames = [first_frame]

    for i in tqdm(range(1, end, step)):
        frame = video.read(i)
        if _mean_squared_error(frame, selected_frames[-1]) < mse_min:
            continue
        else:
            selected_frames.append(frame)

    log.info(
        "Generating the background model using {} frames".format(
            len(selected_frames))
    )

    bgmodel = np.median(
        np.dstack(selected_frames), axis=2).astype(np.uint8)

    return bgmodel


def prepare_output_folder():
    log.info("Preparing the output folder")


def track(video_filepath):
    log.info("Tracking '%s'", video_filepath)
    video = Video(video_filepath)
    prepare_output_folder()
    generate_background_model()
    video.close()

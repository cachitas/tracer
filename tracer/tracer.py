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

        self.background_model = None

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

    def generate_background_model(self, step=None, n=10, mse_min=50):
        """Generates the background model of the video using the median.
        Only sufficiently different frames are considered, using the
        mean squared error method.
        Parameters:
            step: Step to iterate through the video. Default is video FPS rate.
            n: Number of frames to use for the model.
            mse_min: The minimum error at wich the frame is selected. The
                lower the error, the more *similar* the two images are.
        """
        log.info("Generating the background model")

        step = step or int(self.fps)

        log.debug(
            "Selecting frames (step={}, n={}, mse_min={})".format(
                step, n, mse_min)
        )

        progress_bar = tqdm(total=n)
        index = 0
        selected_frames = [self.read(index)]
        progress_bar.update()
        while len(selected_frames) < n:
            index += step
            image = self.read(index)
            if _mean_squared_error(image, selected_frames[-1]) > mse_min:
                selected_frames.append(image)
                progress_bar.update()
        progress_bar.close()

        log.debug(
            "Generating the background model using {} frames".format(
                len(selected_frames))
        )

        self.background_model = np.median(
            np.dstack(selected_frames), axis=2).astype(np.uint8)

    def read(self, index):
        """Read a video frame in grayscale.
        The frame number is stored in the `.meta.index` attribute (imageio).
        """
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


def prepare_output_folder():
    log.info("Preparing the output folder")


def track(video_filepath):
    log.info("Tracking '%s'", video_filepath)
    video = Video(video_filepath)
    prepare_output_folder()
    print(video)
    video.generate_background_model()
    imageio.imwrite(video_filepath[:-4], video.background_model, format='BMP')
    video.close()

import logging
import os
import yaml

import imageio
import numpy as np
import pandas as pd

import cv2
import ocvu

from .video import Video
from .tools import mean_squared_error


logger = logging.getLogger(__name__)


class Tracker:

    def __init__(self):
        # Configuration
        self.video_filepath = ''
        self.number_of_flies = 0
        self.output_folder = ''

        self.background_model = None

    def configure(self, config_file=None, **config):
        """Configure the Tracker using a YAML file or a dictionary."""
        logger.info("Configuring tracker")
        if config_file is not None:
            logger.info("Reading configuration file '%s'", config_file)
            with open(config_file) as f:
                config = yaml.safe_load(f)

        for key, value in config.items():
            logger.debug("Setting %s to %s", key, value)
            self.__setattr__(key, value)

    def count_blobs_per_frame(self, area_min=2000, area_max=3000):
        logger.info("Counting blobs")
        # TODO
        s = pd.Series(index=range(self.video.nframes), name='n')
        for index in range(self.video.nframes)[:50]:
            image = self.video.read(index)
            _, fg_mask = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY_INV)
            blobs = ocvu.find_biggest_contours(fg_mask, n=10)  # TODO use better method
            blobs = [blob for blob in blobs if area_min < blob.area < area_max]
            s.loc[index] = len(blobs)
        print(s)

    def estimate_thresholds(self):
        logger.info("Estimating flies thresholds")

    def generate_background_model(self, step=None, n=6, mse_min=50):
        """Generates the background model of the video using the median.
        Only sufficiently different frames are considered, using the
        mean squared error method.
        Parameters:
            step: Step to iterate through the video. Default is video FPS rate.
            n: Number of frames to use for the model.
            mse_min: The minimum error at wich the frame is selected. The
                lower the error, the more *similar* the two images are.
        """
        logger.info("Generating the background model")

        step = step or int(self.video.fps)

        logger.info(
            "Selecting frames (step={}, n={}, mse_min={})".format(
                step, n, mse_min)
        )

        index = 0
        logger.debug("Using frame %d", index)
        selected_frames = [self.video.read(index)]
        while len(selected_frames) < n:
            index += step
            image = self.video.read(index)
            if mean_squared_error(image, selected_frames[-1]) > mse_min:
                selected_frames.append(image)
                logger.debug("Using frame %d", index)

        logger.info(
            "Generating the background model using {} frames".format(
                len(selected_frames))
        )

        self.background_model = np.median(
            np.dstack(selected_frames), axis=2).astype(np.uint8)

    def run(self):
        """Run the tracker in its current state."""

        logger.info("Running...")

        self.prepare_output_folder()

        self.video = Video(self.video_filepath)

        background_filename = os.path.join(
            self.output_folder, "background.bmp")
        try:
            logger.info("Looking for background model")
            self.background_model = imageio.imread(background_filename)
        except OSError:
            logger.info("Background model not found. Generating new...")
            self.generate_background_model()
            logger.info("Saving background model as '%s'", background_filename)
            imageio.imwrite(
                background_filename, self.background_model, format='BMP')
        else:
            logger.info("Background model found '%s'", background_filename)

        self.count_blobs_per_frame()
        self.estimate_thresholds()

        self.video.close()

    def prepare_output_folder(self):
        """Prepare the output folder."""
        if not self.output_folder:
            video_folder, video_filename = os.path.split(self.video_filepath)
            video_name = os.path.splitext(self.video_filepath)[0]
            self.output_folder = video_name

        logger.info("Preparing the output folder")

        if os.path.exists(self.output_folder):
            logging.info("Output folder already exists")
        else:
            os.mkdir(self.output_folder)
            logger.info("Output folder created")



# def prepare_output_folder():
#     log.info("Preparing the output folder")


# def track():
#     log.info("Tracking '%s'", video_filepath)
#     video = Video(video_filepath)
#     prepare_output_folder()
#     print(video)
#     video.generate_background_model()
#     imageio.imwrite(video_filepath[:-4], video.background_model, format='BMP')
#     video.close()

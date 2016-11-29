import logging
import os
import yaml

import imageio
import numpy as np
import pandas as pd

import cv2

from .io.video import Video
from .io.output import Output
from . import background
from . import tools


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
            logger.debug("Setting %s to %s", repr(key), repr(value))
            self.__setattr__(key, value)

    # def count_blobs_per_frame(self):
    #     logger.info("Counting blobs")

    #     # TODO

    #     result_filepath = os.path.join(self.output_folder, "blob_count.h5")
    #     try:
    #         s = pd.read_hdf(result_filepath)
    #     except OSError as e:
    #         logger.error(e)
    #         s = pd.Series(0, index=range(self.video.nframes), name='n')
    #     except ValueError as e:
    #         logger.error(e)
    #         s = pd.Series(0, index=range(self.video.nframes), name='n')
    #     else:
    #         return

    #     for index in range(self.video.nframes):
    #         if not index % 1000:
    #             logger.info("Processing frame %d", index)

    #         image = self.video.read(index)
    #         foreground = image - self.background_model
    #         _, foreground_mask = cv2.threshold(foreground, 50, 255, cv2.THRESH_BINARY)
    #         foreground_mask = tools.denoise(foreground_mask)

    #         contours = tools.find_biggest_contours(
    #             foreground_mask, n=self.number_of_flies, min_area=1000)

    #         s.loc[index] = len(contours)

    #     # else:
    #     #     # Save last images
    #     #     filename = os.path.join(self.output_folder, "%d.bmp" % index)
    #     #     tools.save(image, filename)
    #     #     filename = os.path.join(self.output_folder, "fg_%d.bmp" % index)
    #     #     tools.save(foreground_mask, filename)

    #     s.to_hdf(result_filepath, key='n')

    # def estimate_thresholds(self):
    #     logger.info("Estimating flies thresholds")
    #     # TODO

    # def generate_background_model(self, step=None, n=6, mse_min=50):
    #     """Generates the background model of the video using the median.
    #     Only sufficiently different frames are considered, using the
    #     mean squared error method.
    #     Parameters:
    #         step: Step to iterate through the video. Default is video FPS rate.
    #         n: Number of frames to use for the model.
    #         mse_min: The minimum error at wich the frame is selected. The
    #             lower the error, the more *similar* the two images are.
    #     """
    #     logger.info("Generating the background model")

    #     step = step or int(self.video.fps)

    #     logger.info(
    #         "Selecting frames (step={}, n={}, mse_min={})".format(
    #             step, n, mse_min)
    #     )

    #     index = 0
    #     logger.debug("Using frame %d", index)
    #     selected_frames = [self.video.read(index)]
    #     while len(selected_frames) < n:
    #         index += step
    #         image = self.video.read(index)
    #         if tools.mean_squared_error(image, selected_frames[-1]) > mse_min:
    #             selected_frames.append(image)
    #             logger.debug("Using frame %d", index)

    #     logger.info(
    #         "Generating the background model using {} frames".format(
    #             len(selected_frames))
    #     )

        # self.background_model = np.median(
        #     np.dstack(selected_frames), axis=2).astype(np.uint8)

    def run(self):
        """Run the tracker in its current state."""

        logger.info("Running...")

        self.video = Video(self.video_filepath)

        self.output = Output(self.video_filepath)

        if self.output.background_model is None:
            background_model = background.compute(self.video)
            self.output.save_image(background_model, 'background_model')

        # self.prepare_output_folder()

        # self.video = Video(self.video_filepath)

        # # self.flies = pd.Panel(
        # #     items=range(self.number_of_flies),
        # #     major_axis=range(self.video.nframes),
        # #     minor_axis=['x', 'y', 'a'],
        # # )

        # background_filename = os.path.join(
        #     self.output_folder, "background.bmp")
        # try:
        #     logger.info("Loading background model '%s'", background_filename)
        #     self.background_model = imageio.imread(background_filename)
        # except OSError:
        #     logger.info("Background model not found. Generating new...")
        #     self.generate_background_model()
        #     logger.info("Saving background model as '%s'", background_filename)
        #     imageio.imwrite(
        #         background_filename, self.background_model, format='BMP')
        # else:
        #     logger.info("Background model found '%s'", background_filename)

        # self.count_blobs_per_frame()
        # # self.segment_flies()
        # self.estimate_thresholds()

        # self.video.close()

        logger.info("Finished")

    # def prepare_output_folder(self):
    #     """Prepare the output folder."""
    #     if not self.output_folder:
    #         video_folder, video_filename = os.path.split(self.video_filepath)
    #         video_name = os.path.splitext(self.video_filepath)[0]
    #         self.output_folder = video_name

    #     logger.info("Preparing the output folder")

    #     if os.path.exists(self.output_folder):
    #         logger.info("Output folder already exists")
    #     else:
    #         os.mkdir(self.output_folder)
    #         logger.info("Output folder created")

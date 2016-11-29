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

    def run(self):
        """Run the tracker in its current state."""

        logger.info("Running...")

        self.video = Video(self.video_filepath)

        self.output = Output(self.video_filepath)

        if self.output.background_model is None:
            background_model = background.compute(self.video)
            self.output.save_image(background_model, 'background_model')

        logger.info("Finished")

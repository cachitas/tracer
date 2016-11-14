import logging
import os
import yaml

import imageio
import numpy as np
from tqdm import tqdm, trange

from .video import Video


logger = logging.getLogger(__name__)


class Tracker:

    def __init__(self):
        # Configuration
        self.video_filepath = ''
        self.number_of_flies = 0
        self.output_folder = ''

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

    def run(self):
        """Run the tracker in its current state."""
        logger.info("Running")
        self.prepare_output_folder()
        self.video = Video(self.video_filepath)
        print(self.video)
        self.video.close()

    def prepare_output_folder(self):
        """Prepare the output folder."""
        if not self.output_folder:
            video_folder, video_filename = os.path.split(self.video_filepath)
            video_name = os.path.splitext(self.video_filepath)[0]
            self.output_folder = video_name

        logger.info("Preparing the output folder")

        if os.path.exists(self.output_folder):
            msg = "Output folder exists"
            logging.critical(msg)
            raise SystemExit("Tracker aborted: %s" % msg)
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

import logging
import multiprocessing as mp
import os
import yaml

import imageio
import numpy as np
import pandas as pd

import cv2

from .io.video import Video
from .io.output import Output
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

        output = Output(self.video_filepath)

        if output.background is None:
            background = compute_background_model(self.video)
            output.save_image(background, 'background')

        if output.blobs is None:
            tasks = [
                (
                    self.video,
                    chunk,
                    segment_blobs,
                    dict(
                        background=output.background,
                        n=self.number_of_flies,
                        min_area=self.area
                    )
                )
                for chunk in tools.split_in_chunks(self.video.frames, 8)
            ]

            processes = min(len(tasks), mp.cpu_count())
            logger.info("Spawning %d processes", processes)
            with mp.Pool(processes) as pool:
                blobs = pool.starmap(process, tasks)
            blobs = pd.concat(blobs)

            output.save_hdf(blobs, 'blobs')

        logger.info("Finished")


def compute_background_model(video, step=None):
    """Compute the background model of a video."""
    # TODO need to externally control the thresholds used for MSE

    logger.info("Computing the background model")

    step = step or video.fps
    background_model = None
    distinct_frames = []
    bg = None
    bg_updated = None

    logger.debug("Reading frames in steps of %d frames", step)

    index = 0
    distinct_frames.append(video.get(index))
    bg = distinct_frames[-1]

    while background_model is None and index < step * 100:
        index += step
        previous_image = distinct_frames[-1]
        image = video.get(index)
        mse = tools.mean_squared_error(previous_image, image)
        logger.debug("MSE=%.1f", mse)
        if mse > 50:  # TOFIX
            distinct_frames.append(image)
        else:
            continue
        bg_updated = np.median(
            np.dstack(distinct_frames), axis=2).astype(np.uint8)
        bg_mse = tools.mean_squared_error(bg, bg_updated)
        logger.debug(
            "Updating the background model using %d frames (MSE: %.1f)",
            len(distinct_frames), bg_mse
        )
        if bg_mse < 0.5:  # TOFIX
            background_model = bg_updated
        else:
            bg = bg_updated

    return background_model


def process(video, frames, func, func_args):
    logger.info("Processing frames [%5d, %5d]", frames[0], frames[-1])
    df = pd.DataFrame()
    for image in video.get_chunk(frames):
        s = func(image, **func_args)
        df = df.append(s.to_frame().T)
    return df


def segment_blobs(image, background, n, min_area):
    """Segment blobs in an image."""

    frame_number = image.meta.index

    logger.debug("Segmenting blobs in frame %d", frame_number)
    cols = ['c%d_%s' % (i, feat) for i in range(n) for feat in 'xywh']
    s = pd.Series(0, index=['n'] + cols, name=frame_number)

    fg = image - background
    _, fg_mask = cv2.threshold(fg, 10, 255, cv2.THRESH_BINARY)
    fg_mask = tools.denoise(fg_mask, 7)
    contours = tools.find_biggest_contours(fg_mask, n, min_area)
    s.loc['n'] = len(contours)
    for i, c in enumerate(contours):
        x, y, w, h = c.bounding_box
        s.loc['c%d_x' % i] = x
        s.loc['c%d_y' % i] = y
        s.loc['c%d_w' % i] = w
        s.loc['c%d_h' % i] = h

    return s

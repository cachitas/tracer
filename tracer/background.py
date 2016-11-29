import logging

import numpy as np

from . import tools

logger = logging.getLogger(__name__)


def compute(video, step=None):
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


if __name__ == '__main__':
    from .io.video import Video

    logging.basicConfig(level=logging.DEBUG)

    video = Video('sample_videos/single.avi')
    print(video)

    bg = compute(video)
    print(bg)

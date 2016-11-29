from contextlib import contextmanager
import logging

import imageio
import numpy as np

logger = logging.getLogger(__name__)


class Video:

    def __init__(self, filepath):
        self.filepath = filepath

        with self.get_reader() as reader:
            logger.info("Reading video metadata")
            self.metadata = reader.get_meta_data()

    def __str__(self):
        return "Video('{}', size={s}, nframes={n}, fps={fps})".format(
            self.filepath,
            s=self.size,
            n=self.nframes,
            fps=self.fps
        )

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

    @property
    def frames(self):
        """Returns an iterator with all frames."""
        return np.arange(self.nframes)

    @contextmanager
    def get_reader(self):
        """Custom wrapper around `imageio.get_reader()` using FFMPEG"""
        logger.debug("Opening imageio.Reader")
        yield imageio.get_reader(self.filepath, format='FFMPEG', mode='I')
        logger.debug("Closing imageio.Reader")

    def _get(self, reader, index):
        """Provides a common interface to all reading operations.
        Assuming the video is in grayscale, only one color channel is returned.
        The frame number is stored in the `.meta.index` attribute (imageio).
        """
        logger.debug("Reading frame %d", index)
        image = reader.get_data(index)
        image = image[:, :, 1]
        image.meta.index = index
        return image

    def get(self, index):
        with self.get_reader() as reader:
            return self._get(reader, index)

    def get_chunk(self, chunk):
        with self.get_reader() as reader:
            for index in chunk:
                yield self._get(reader, index)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    video = Video('sample_videos/single.avi')

    img = video.get(10)

    chunk = np.arange(10)
    for img in video.get_chunk(chunk):
        pass

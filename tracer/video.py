import logging

import imageio


log = logging.getLogger(__name__)


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
        image = self.reader.get_data(index)
        image = image[:, :, 1]
        image.meta.index = index
        return image

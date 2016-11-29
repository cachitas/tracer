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





# class Video:
#     """Custom wrapper around `imageio.Reader` using FFMPEG"""

#     def __init__(self, filepath):
#         self.filepath = filepath

#         logger.debug("Opening imageio.Reader")
#         self.reader = imageio.read(
#             uri=self.filepath,
#             format='FFMPEG',
#             mode='I',
#         )

#         logger.debug("Reading video metadata")
#         self.metadata = self.reader.get_meta_data()

#     def __str__(self):
#         return "Video('{}', size={s}, nframes={n}, fps={fps})".format(
#             self.filepath,
#             s=self.size,
#             n=self.nframes,
#             fps=self.fps
#         )

#     def __del__(self):
#         logger.debug("Closing imageio.Reader")
#         self.reader.close()

#     # def __open(self):
#     #     logger.debug("Opening imageio.Reader")
#     #     self._reader = imageio.get_reader(
#     #         uri=self.filepath,
#     #         format='FFMPEG',
#     #         mode='I',
#     #     )

#     # def __close(self):
#     #     logger.debug("Closing imageio.Reader")
#     #     self._reader.close()

#     @property
#     def fps(self):
#         """Returns the frame rate as a float"""
#         return self.metadata['fps']

#     @property
#     def nframes(self):
#         """Returns the number of frames as an int"""
#         return self.metadata['nframes']

#     @property
#     def size(self):
#         """Returns a tuple with (width, height)."""
#         return self.metadata['size']

#     @property
#     def frames(self):
#         """Returns an iterator with all frames."""
#         return np.arange(self.nframes)

#     def _read(self, index):
#         """Provides a common interface to all reading operations.
#         Assuming the video is in grayscale, only one color channel is returned.
#         The frame number is stored in the `.meta.index` attribute (imageio).
#         """
#         logger.debug("Reading frame %d", index)
#         image = self.reader.get_data(index)
#         image = image[:, :, 1]
#         image.meta.index = index
#         return image

#     def get(self, index):
#         # self.__open()
#         # image = self._read(index)
#         # self.__close()
#         # return image
#         return self._read(index)

#     # def iter_chunk(self, chunk):
#     #     self.__open()
#     #     for index in chunk:
#     #         yield self._read(index)
#     #     self.__close()

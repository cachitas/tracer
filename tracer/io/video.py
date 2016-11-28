import logging

import imageio
import numpy as np

logger = logging.getLogger(__name__)


def get_reader(uri):
    """Custom wrapper around `imageio.get_reader()` using FFMPEG"""
    return imageio.get_reader(uri, format='FFMPEG', mode='I')


def get_metadata(uri):
    logger.info("Reading video metadata")
    with get_reader(uri) as reader:
        metadata = reader.get_meta_data()


def read(reader, index):
    logger.debug("Reading frame %d", index)
    image = reader.get_data(index)
    image = image[:, :, 1]
    image.meta.index = index
    return image


class Video:

    def __init__(self, filepath):
        self.filepath = filepath
        self.reader = get_reader(self.filepath)

    def read(self, index):
        logger.debug("Reading frame %d", index)
        image = self.reader.get_data(index)
        image = image[:, :, 1]
        image.meta.index = index
        return image


# FIXME all of it!


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    video = Video('sample_videos/single.avi')

    with video.reader as reader:
        print(reader.read(0))

    # img = video.get(10)
    # print(img.meta.index, img.shape)

    # chunk = np.arange(20, 22)
    # for img in video.iter_chunk(chunk):
    #     print(img.meta.index, img.shape)






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

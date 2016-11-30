import logging
import os

import imageio
import pandas as pd

logger = logging.getLogger(__name__)


class Output:

    IMG_EXT = 'bmp'
    HDF_EXT = 'h5'

    def __init__(self, video_filepath=None, path=None):

        if not any([video_filepath, path]):
            raise ValueError("Must provide at least one path")

        if video_filepath:
            self.path = os.path.splitext(video_filepath)[0]
        else:
            self.path = path

        if os.path.exists(self.path):
            logger.debug("An existing output folder was found")
        else:
            logger.debug("Creating folder '%s'", self.path)
            os.mkdir(self.path)

        logger.info("Output folder set to '%s'", self.path)

        self.background = self.load_image('background')
        self.blobs = self.load_hdf('blobs')

    def __repr__(self):
        return "Output(path={})".format(repr(self.path))

    def _build_filepath(self, filename, extension):
        return os.path.join(self.path, filename + '.' + extension)

    def load_hdf(self, filename):
        filepath = self._build_filepath(filename, self.HDF_EXT)
        try:
            logger.info("Loading HDF '%s'", filepath)
            df = pd.read_hdf(filepath)
        except FileNotFoundError as e:
            logger.error(e)
            df = None
        return df

    def load_image(self, filename):
        filepath = self._build_filepath(filename, self.IMG_EXT)
        try:
            logger.info("Loading image '%s'", filepath)
            image = imageio.imread(filepath)
        except OSError as e:
            logger.error(e)
            image = None
        return image

    def save_hdf(self, df, filename='df'):
        if self.__getattribute__(filename) is None:
            logger.debug("Setting output attribute '%s'", filename)
            self.__setattr__(filename, df)
        filepath = self._build_filepath(filename, self.HDF_EXT)
        logger.info("Saving DataFrame as HDF to %s", repr(filepath))
        df.to_hdf(filepath, '/'+filename)

    def save_image(self, image, filename='image', format=None):
        if self.__getattribute__(filename) is None:
            logger.debug("Setting output attribute '%s'", filename)
            self.__setattr__(filename, image)
        filepath = self._build_filepath(filename, (format or self.IMG_EXT))
        logger.info("Saving image %s", repr(filepath))
        imageio.imwrite(filepath, image, format=(format or self.IMG_EXT))

    def clear(self):
        try:
            os.rmdir(self.path)
        except OSError as e:
            logger.exception(e)
        else:
            logger.info("Output folder %s removed", self.path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    o = Output('sample_videos/single.avi')
    o.clear()

    o = eval(repr(o))
    o.clear()

    o = Output(path=o.path)
    o.clear()

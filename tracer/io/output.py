import logging
import os

logger = logging.getLogger(__name__)


class Output:

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


    def __repr__(self):
        return "Output(path={})".format(repr(self.path))

    def load_image(name, format='BMP'):
        raise NotImplementedError

    def save_image(image):
        raise NotImplementedError

    def clear(self):
        try:
            os.rmdir(self.path)
        except OSError as e:
            logger.error(e)
            raise
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

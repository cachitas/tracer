import logging

import imageio
import pylab as pl
from tqdm import tqdm


class LoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super(self.__class__, self).__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def savefig(filename, image, format='BMP'):
    if not filename.lower().endswith(format.lower()):
        filename += '.%s' % format.lower()
    imageio.imwrite(filename, image, format=format)


def imshow(image, title=""):
    pl.figure()
    pl.title(title)
    pl.imshow(image)
    pl.show()

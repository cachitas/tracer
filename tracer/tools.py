import logging

import imageio
import numpy as np
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


def _mean_squared_error(img1, img2):
    """
    The **Mean Squared Error** between the two images is the sum of the
    squared difference between the two images. The lower the error, the
    more *similar* the two images are.
    **NOTE:** the two images must have the same dimension.
    """
    err = np.sum((img1.astype('float') - img2.astype('float')) ** 2)
    err /= float(img1.shape[0] * img1.shape[1])
    return err

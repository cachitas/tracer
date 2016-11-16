import logging

import cv2
import imageio
import numpy as np
import matplotlib.pyplot as plt

from .contour import Contour


logger = logging.getLogger(__name__)


def save(image, filename, format='BMP'):
    """Save an image."""
    if not filename.lower().endswith(format.lower()):
        filename += '.%s' % format.lower()
    imageio.imwrite(filename, image, format=format)


def show(image, title=""):
    """Uses matplotlib to show an image and its histogram."""
    fig, axs = plt.subplots(ncols=2)
    plt.title(title)
    im = axs[0].imshow(image, cmap='viridis')
    plt.colorbar(im, ax=axs[0], orientation='horizontal', ticks=np.linspace(0, 255, 2))
    hist = np.bincount(image.ravel(), minlength=256)
    axs[1].plot(np.arange(len(hist))+.5, hist)
    axs[1].set_xlim(0, 255)
    plt.tight_layout()
    plt.show()


def mean_squared_error(image_1, image_2):
    """
    The **Mean Squared Error** between the two images is the sum of the
    squared difference between the two images. The lower the error, the
    more *similar* the two images are.
    **NOTE:** the two images must have the same dimension.
    """
    err = np.sum((image_1.astype('float') - image_2.astype('float')) ** 2)
    err /= float(image_1.shape[0] * image_1.shape[1])
    return err


def denoise(image, size=3):
    """Removes noise from an image."""
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel(size))


def find_biggest_contours(image, n=1, min_area=None, **kwargs):
    """Returns the `n` biggest contours in `image`.
    Returns a list of contours sorted by area in descending order.
    If you provide a minimal area value, contours returned will be
    filtered like so.
    """
    image = image.copy()  # so findContours does not modify the original
    mode = kwargs.pop('mode', cv2.RETR_EXTERNAL)
    method = kwargs.pop('method', cv2.CHAIN_APPROX_SIMPLE)
    _, contours, _ = cv2.findContours(image.copy(), mode, method, **kwargs)
    contours_found = list(map(Contour, contours))
    if min_area is not None:
        contours = [cnt for cnt in contours_found if cnt.area > min_area]
    else:
        contours = list(contours_found)
    contours.sort(key=lambda cnt: cnt.area, reverse=True)
    contours = contours[:n]
    logger.debug("Retrieved {} contours from {} found".format(
        len(contours), len(contours_found)))
    return contours


def kernel(size):
    """Returns a circular kernel."""
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))

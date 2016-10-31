from collections import namedtuple

import imageio
from skimage import exposure
import pylab


class Video:

    def __init__(self, filename):
        self.filename = filename
        self.reader = imageio.get_reader(filename, format='FFMPEG', mode='I')
        self.metadata = self.reader.get_meta_data()

    def __str__(self):
        s = "Video:\n"
        template = "\t{item:14}: {text}\n"
        s += template.format(item="source", text=self.filename)
        for key, value in self.metadata.items():
            s += template.format(item=key, text=value)
        return s

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

    def read(self, number):
        """Read a video frame.
        """
        if number:
            data = self.reader.get_data(index=number)
        else:
            data = self.reader.get_next_data()
        return Frame(number, data)


class Frame(namedtuple('Frame', ['number', 'image'])):

    __slots__ = ()

    def __str__(self):
        return "Frame(number=%d)" % self.number

    @property
    def gray(self):
        return self.image[:, :, 1]


if __name__ == '__main__':
    filename = 'sample_videos/couple.avi'

    video = Video(filename)
    print(video)

    f = video.read(0)
    print(f)
    print(f.gray)
    # del f

    hist, bin_centers = exposure.histogram(f.gray)

    img = f.gray
    # img_eq = exposure.equalize_hist(img)
    img_eq = exposure.equalize_adapthist(img)

    fig, axs = pylab.subplots(2, 2)
    axs[0, 0].imshow(img, cmap='viridis')

    hist, bin_centers = exposure.histogram(img)
    axs[0, 1].plot(hist)

    axs[1, 0].imshow(img_eq, cmap='viridis')

    hist, bin_centers = exposure.histogram(img_eq)
    axs[1, 1].plot(hist)

    pylab.show()

    del video  # without this it hangs randomly on exit

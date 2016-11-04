from collections import namedtuple

import imageio
import pylab as pl


class Video:

    def __init__(self, filename):
        self.filename = filename
        self.reader = imageio.get_reader(filename, format='FFMPEG', mode='I')
        self.metadata = self.reader.get_meta_data()

    def __del__(self):
        self.reader.close()
        super().__del__()
        # del self.reader

    # def __str__(self):
    #     s = "Video:\n"
    #     template = "\t{item:14}: {text}\n"
    #     s += template.format(item="source", text=self.filename)
    #     for key, value in self.metadata.items():
    #         s += template.format(item=key, text=value)
    #     s = "Video"
    #     return s

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


def imshow(image, title=""):
    pl.figure()
    pl.title(title)
    pl.imshow(image)
    pl.show()

import imageio
import numpy as np


class Video:

    def __init__(self, filename):
        self.filename = filename
        self.reader = imageio.get_reader(filename, format='FFMPEG', mode='I')
        self.metadata = self.reader.get_meta_data()

    def __get__(self, instance, value):
        return self.reader

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


class Frame(np.ndarray):

    def __new__(cls, input_array, number=None):
        obj = np.asarray(input_array).view(cls)
        obj.number = number
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.number = getattr(obj, 'info', None)


def load_video(filename, nframes=None):
    with imageio.get_reader(uri=filename, format='FFMPEG') as reader:
        metadata = reader.get_meta_data()
        width, height = metadata['source_size']
        fps = metadata['fps']
        nframes = min([nframes or metadata['nframes'], metadata['nframes']])
        video = np.zeros(shape=(nframes, width, height), dtype=np.uint8)
        print("Loading video with shape", video.shape)
        for index, image in enumerate(reader):
            image = image[:, :, 1]
            try:
                video[index] = image
            except IndexError:
                break
        return video, fps

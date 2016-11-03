import imageio
import numpy as np


class Video:

    def __init__(self, data, fps):
        self._data = data
        self.fps = fps

    def __get__(self):
        return self._data


def load_video(filename, nframes=None):
    with imageio.get_reader(uri=filename, format='FFMPEG') as reader:
        metadata = reader.get_meta_data()
        print(metadata)
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

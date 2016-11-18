import imageio
from queue import Queue

filepath = 'sample_videos/single.avi'


class VideoReader:

    def __init__(self):
        pass

    def start(self, first=0):
        """Start reading frames and queue them."""

    def stop(self):
        """Stop."""


with imageio.get_reader(filepath, format='FFMPEG', mode='I') as reader:
    metadata = reader.get_meta_data()
    nframes = metadata['nframes']

    q = Queue()

    for image in reader:
        q.put(image)

        print(q.qsize())

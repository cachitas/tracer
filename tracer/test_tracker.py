import logging

from .io.video import Video
from .tools import show
from .tracker import compute_background_model


def test_compute_background_model():
    video = Video('sample_videos/single.avi')
    bg = compute_background_model(video)
    show(bg)


def test_segment_blobs():
    raise NotImplementedError


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    test_compute_background_model()

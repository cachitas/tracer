import logging

from .io.video import Video
from .io.output import Output
from .tools import show
from .tracker import compute_background_model
from .tracker import segment_blobs


video1 = Video('sample_videos/single.avi')
video2 = Video('sample_videos/couple.avi')


def test_compute_background_model():
    bg = compute_background_model(video1)
    show(bg)


def test_segment_blobs():
    v = video2
    out = Output(v.filepath)
    bg = out.background

    image = v.get(22100)

    s = segment_blobs(image, bg, 2, 500)
    print(s)

    x, y, w, h = s[1:5]

    blob = image[y:y + h, x:x + w]

    show(image)
    show(blob)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    logging.info("Running selected tests")

    # test_compute_background_model()
    test_segment_blobs()

    logging.info("Finished")

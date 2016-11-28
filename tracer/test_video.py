# import os
# import pytest
# import numpy as np
# from .tracer import Video


# @pytest.fixture
# def video_1(request):
#     filename = os.path.join('sample_videos', 'single.avi')
#     video = Video(filename)

#     def close():
#         video.close()

#     request.addfinalizer(close)
#     return video


# def test_video_metadata(video_1):
#     assert video_1.size == (1024, 1024)
#     assert video_1.fps == 60
#     assert video_1.nframes == 7881


# def test_read_frame(video_1):
#     frame_number = 9
#     frame = video_1.read(frame_number)
#     assert frame.meta.index == frame_number
#     assert frame.shape == (1024, 1024)
#     assert frame.dtype == np.uint8



class Video:

    def __init__(self, filepath):
        self.filepath = filepath
        self.reader = imageio.get_reader(filepath, format='FFMPEG', mode='I')
        self.metadata = self.reader.get_meta_data()
        self.frames = np.zeros(shape=(self.nframes, *self.size), dtype=np.uint8)

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

    def close(self):
        """Close the reader object."""
        self.reader.close()

    # def load(self):
    #     # FIXME remove me maybe
    #     # Loads the video in memory, populating the `frames` array.
    #     for index in trange(self.nframes):
    #         self.read(index)

    def read(self, index):
        """Read a video frame in grayscale.
        The obtained image is cached and returned.
        The frame number is stored in the `.meta.index` attribute (imageio).
        """
        image = self.frames[index]
        if np.count_nonzero(image) == 0:
            image = self.reader.get_data(index)
            image = image[:, :, 1]
            image.meta.index = index
            self.frames[index] = image
        return image

    # def save(self):
    #     # FIXME remove me maybe
    #     """Saves the `frames` array to a file."""
    #     log.info("Saving binary data for video '%s'. Please wait...", self.filename)
    #     np.save(self.filename, self.frames, allow_pickle=False)



# def load_video(filename):
#     # FIXME this is not doable.. videos become too large
#     """Load the entire video into memory.
#     Tries to open a binary file in `.npy` format first.
#     """
#     video = Video(filename)
#     log.info("Loading binary data for video '%s'. Please wait...", filename)
#     try:
#         frames = np.load(filename + '.npy')
#     except FileNotFoundError as e:
#         log.error(e)
#         log.info("Reading original video")
#         video.load()
#         # video.save()
#     else:
#         video.frames = frames
#     finally:
#         assert video.frames.shape == (video.nframes, *video.size)
#     video.close()
#     return video

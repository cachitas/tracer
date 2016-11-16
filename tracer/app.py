from kivy.app import App
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.image import Image

from .tracker import Tracker
from .video import Video


class NumpyImage(Image):
    """Display a numpy image."""

    data = ObjectProperty(None)

    def on_data(self, *args):
        """Load image from memory."""
        self.texture = self.data.tostring()


class TracerApp(App):

    index = NumericProperty()
    img_original = ObjectProperty()
    img_foreground = ObjectProperty()

    def build(self):
        tracker = Tracker()
        tracker.configure('config_sample_2.yml')
        self.video = Video(tracker.video_filepath)

        self.img_original = self.video.read(0)

    def set_image(self, index):
        image = self.video.read(index)
        print(image)
        print(self.img_original)
        self.img_original = image
        # FIXME


if __name__ == '__main__':
    TracerApp().run()

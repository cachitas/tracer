from kivy.app import App
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty

from .tracker import Tracker
from .video import Video


class TracerApp(App):

    index = NumericProperty()
    img_original = ObjectProperty()
    img_foreground = ObjectProperty()

    def build(self):
        tracker = Tracker()
        tracker.configure('config_sample_2.yml')
        self.video = Video(tracker.video_filepath)

    def set_image(self, index):
        image = self.video.read(index)
        print(image)
        self.img_original.texture
        # FIXME


if __name__ == '__main__':
    TracerApp().run()

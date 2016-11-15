import pandas as pd


class Drosophila:

    def __init__(self):
        self.df = pd.DataFrame(index='time', columns=list('xya'))

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, value):
        self.x, self.y = value

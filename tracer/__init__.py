import pandas as pd
import pylab as pl


if __name__ == '__main__':
    s = pd.read_csv('nblobs.csv', index_col=0)
    s.plot()
    pl.show()

import pylab as pl


def imshow(image, title=""):
    pl.figure()
    pl.title(title)
    pl.imshow(image)
    pl.show()

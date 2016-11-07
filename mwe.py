import imageio

r = imageio.get_reader('sample_videos/single.avi', format='FFMPEG')
# print(r.get_meta_data())
# img = r.get_data()
# print(img.shape)
# r.close()
a = r.get_data(0)
a = a[:, :, 1]
a.meta.index = 0
print(a)
print(a.meta)
print(a.__dict__)
r.close()

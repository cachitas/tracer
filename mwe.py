import imageio

r = imageio.get_reader('cockatoo.mp4', format='AVBIN')
# print(r.get_meta_data())
# img = r.get_data()
# print(img.shape)
# r.close()
a = r.get_data(0)
print(a)
r.close()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .io.output import Output

output = Output('sample_videos/couple.avi')

df = output.blobs

print("Value counts:")
print(df.n.value_counts())

df.n.plot()
plt.ylim(0, df.n.max()+1)
plt.show()

fig, axs = plt.subplots(ncols=df.n.max()+1, sharex=True, sharey=True)

i = 0

for n in sorted(df.n.unique()):

    if n == 0:
        continue

    print("Frames where %d blobs were detected" % n)

    dfn = df[df.n == n].copy()
    print(dfn.describe())

    for j in range(n):
        print("Plotting contour %d on axes %d" % (j, i+j))

        sns.kdeplot(dfn['c%d_w' % j], dfn['c%d_h' % j],
                    shade=True, shade_lowest=False, ax=axs[i+j])

    i += 1


for ax in axs:
    ax.set(aspect='equal', xlim=(20, 220), ylim=(20, 220), adjustable='box-forced')

plt.show()
exit()


# fig, axs = plt.subplots(ncols=3, sharex=True, sharey=True)

# sns.kdeplot(df1.c0_w, df1.c0_h,
#             cmap='Greens', shade=True, shade_lowest=False, ax=axs[0])
# sns.kdeplot(df2.c0_w, df2.c0_h,
#             cmap='Blues', shade=True, shade_lowest=False, ax=axs[1])
# sns.kdeplot(df2.c1_w, df2.c1_h,
#             cmap='Reds', shade=True, shade_lowest=False, ax=axs[2])

# for ax in axs:
#     # ax.set_aspect('equal')
#     ax.set_ylim(40, 220)

# fig, axs = plt.subplots(nrows=2, sharex=True, sharey=True)
# sns.distplot(df2.c0_a, color='b', ax=axs[0])
# sns.distplot(df2.c1_a, color='r', ax=axs[1])
# plt.show()

# print(df.c0_a.describe())
#

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_hdf('blobs.h5')

print(df.n.value_counts())

# df.n.plot()
# plt.ylim(0, df.n.max()+1)
# plt.show()

df1 = df[df.n == 1].copy()
df2 = df[df.n == 2].copy()

print(df1.describe())
print(df2.describe())

fig, axs = plt.subplots(ncols=3, sharex=True, sharey=True)


sns.kdeplot(df1.c0_w, df1.c0_h,
            cmap='Greens', shade=True, shade_lowest=False, ax=axs[0])
sns.kdeplot(df2.c0_w, df2.c0_h,
            cmap='Blues', shade=True, shade_lowest=False, ax=axs[1])
sns.kdeplot(df2.c1_w, df2.c1_h,
            cmap='Reds', shade=True, shade_lowest=False, ax=axs[2])

for ax in axs:
    # ax.set_aspect('equal')
    ax.set_ylim(40, 220)

fig, axs = plt.subplots(nrows=2, sharex=True, sharey=True)
sns.distplot(df2.c0_a, color='b', ax=axs[0])
sns.distplot(df2.c1_a, color='r', ax=axs[1])
plt.show()

# print(df.c0_a.describe())
#

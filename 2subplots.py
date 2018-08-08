#fig, ax_lst = plt.subplots(1, 2)  # a figure with a 2x2 grid of Axes
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('title')  # Add a title so we know which it is
imgplot1 = ax1.imshow(img, cmap="jet",origin='lower')
img2=img*fabs[imageindex_init];
imgplot2 = ax2.imshow(img2, cmap="jet",origin='lower')


imgplot1.norm=colors.LogNorm(1,img.max())
imgplot2.norm=colors.LogNorm(1,img.max())
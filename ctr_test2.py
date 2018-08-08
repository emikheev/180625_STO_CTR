import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.widgets import Slider

basename='P2015_06_06_CTR4_00L_scan1_';
folder='C:/SSRL/May2017/P2015_06_06';
folderraw='C:/SSRL/May2017/PilatusAll'

imageindex_init=31;
imageindex_min = 1    # the minimial value of the paramater a
imageindex_max = 50   # the maximal value of the paramater a

strimageindex = '%(#)04i' % \
{"#": imageindex_init}
filenameraw=folderraw+'/b_mehta_'+basename+strimageindex+'.raw'

 
#OpenPilatusImage .raw


fig = plt.figure(figsize=(12,5))

f1 = open(filenameraw, "r")
raw = np.fromfile(f1, dtype=np.uint32)
img=raw.reshape(195,487)
f1.close()

img[0:3,0:3] = 0;img[194,0] = 0;img[0,486] = 0;img[194,486] = 0; img[img > 4.2e9] = 0;

#imgplot = plt.imshow(np.log10(img), cmap="jet",origin='lower');

imgplot = plt.imshow(img, cmap="jet",origin='lower',norm=colors.LogNorm(1,img.max()));
plt.colorbar();
db=[245,118];

plt.plot(db[0]*np.ones(194),np.arange(0,194),'k:')
plt.plot(np.arange(0,486),db[1]*np.ones(486),'k:')

slider_ax = plt.axes([0, 0.05, 0.8, 0.05])

img_slider = Slider(slider_ax,      # the axes object containing the slider
                  'imageindex',            # the name of the slider parameter
                  imageindex_min,          # minimal value of the parameter
                  imageindex_max,          # maximal value of the parameter
                  valinit=imageindex_init,  # initial value of the parameter
                  valstep=1.0
                 )

def update(imageindex):
    #sin_plot.set_ydata(np.sin(a*x)) # set new y-coordinates of the plotted points
    #fig.canvas.draw_idle()          # redraw the plot
    
    strimageindex = '%(#)04i' % \
    {"#": imageindex}
    filenameraw=folderraw+'/b_mehta_'+basename+strimageindex+'.raw';
    f1 = open(filenameraw, "r")
    raw = np.fromfile(f1, dtype=np.uint32)
    img=raw.reshape(195,487)
    f1.close()
    img[0:3,0:3] = 0;img[194,0] = 0;img[0,486] = 0;img[194,486] = 0; img[img > 4.2e9] = 0;
    imgplot.set_data(img)
    imgplot.norm=colors.LogNorm(1,img.max())
    display(filenameraw)
    #imgplot = plt.imshow(img, cmap="jet",origin='lower',norm=colors.LogNorm(10,img.max()));

# the final step is to specify that the slider needs to
# execute the above function when its value changes
img_slider.on_changed(update)

plt.show()
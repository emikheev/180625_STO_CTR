import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.widgets import Slider

basename='HKLscan2_BPBO114_scan1';
#basename='HKLscan44_BPBO1p5m0p53p5_scan1';
#basename='HKLscan59_BPBO0p503p5_scan1';
#basename='HKLscan62_BPBO0p5m13p5_scan1';
#basename='HKLscan60_BPBOm0p503p5_scan1';
#basename='HKLscan64_BPBO00p52p5_scan1';

folder='C:/SSRL/Jul2018/1_phi0';
folderraw='C:/SSRL/Jul2018/1_phi0/Pilatus'

strimageindex = '%(#)04i' % \
{"#": imageindex_init}
filenameraw=folderraw+'/b_mehta_'+basename+'_'+strimageindex+'.raw'

#get CSV
filenameCSV=folder+'/'+basename+'.csv'

from numpy import genfromtxt
dataCSV = np.genfromtxt(filenameCSV, delimiter=',')
foils=dataCSV[:,13];

 
#OpenPilatusImage .raw

imageindex_init=0;
imageindex_min = 0;
imageindex_max = dataCSV.shape[0]-1;

fig = plt.figure(figsize=(12,5))

f1 = open(filenameraw, "r")
raw = np.fromfile(f1, dtype=np.uint32)
img=raw.reshape(195,487)
f1.close()
img[0:3,0:3] = 0;img[194,0] = 0;img[0,486] = 0;img[194,486] = 0; img[img > 4.2e9] = 0;

#imgplot = plt.imshow(np.log10(img), cmap="jet",origin='lower');
#imgplot = plt.imshow(img, cmap="jet",origin='lower',norm=colors.LogNorm(1,img.max()));
imgplot = plt.imshow(img, cmap="jet",origin='lower')
plt.title(basename+', imageindex = '+str(imageindex_init))

imgplot.norm=colors.LogNorm(1,img.max())
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
    ax=imgplot;
    strimageindex = '%(#)04i' % \
    {"#": imageindex}
    filenameraw=folderraw+'/b_mehta_'+basename+'_'+strimageindex+'.raw';
    f1 = open(filenameraw, "r")
    raw = np.fromfile(f1, dtype=np.uint32)
    img=raw.reshape(195,487)
    f1.close()
    img[0:3,0:3] = 0;img[194,0] = 0;img[0,486] = 0;img[194,486] = 0; img[img > 4.2e9] = 0;
    imgplot.set_data(img)
    imgplot.norm=colors.LogNorm(1,img.max())
    #imgplot.cmap="jet";
    #plt.colorbar();
    plt.title(basename+', imageindex = '+str(imageindex))
    #imgplot = plt.imshow(img, cmap="jet",origin='lower',norm=colors.LogNorm(10,img.max()));

# the final step is to specify that the slider needs to
# execute the above function when its value changes
img_slider.on_changed(update)

plt.show()
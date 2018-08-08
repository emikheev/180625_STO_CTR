import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.widgets import Slider

plt.close("all")
basename='HKLscan2_BPBO114_scan1';
#basename='HKLscan44_BPBO1p5m0p53p5_scan1';
#basename='HKLscan59_BPBO0p503p5_scan1';
#basename='HKLscan62_BPBO0p5m13p5_scan1';
#basename='HKLscan60_BPBOm0p503p5_scan1';
#basename='HKLscan64_BPBO00p52p5_scan1';

folder='C:/SSRL/Jul2018/1_phi0';
folderraw='C:/SSRL/Jul2018/1_phi0/Pilatus'

imageindex_init=390;
strimageindex = '%(#)04i' % \
{"#": imageindex_init}
filenameraw=folderraw+'/b_mehta_'+basename+'_'+strimageindex+'.raw'

#get CSV
filenameCSV=folder+'/'+basename+'.csv'

#from numpy import genfromtxt
dataCSV = np.genfromtxt(filenameCSV, delimiter=',')


abs=[0.87, 2.470, 3.770, 10.830]
foils=dataCSV[:,13];
fabs=list()
for i in range(0, len(dataCSV)):
    foils=int(dataCSV[i,13])
    a=f"{foils:04d}"
    abs=[0.87, 2.470, 3.770, 10.830]
    #fabs[i]=1/np.exp(-int(a[0])*abs[0]-int(a[1])*abs[1]-int(a[2])*abs[2]-int(a[3])*abs[3])
    fabs.append(1/np.exp(-int(a[0])*abs[0]-int(a[1])*abs[1]-int(a[2])*abs[2]-int(a[3])*abs[3]))
#OpenPilatusImage .raw


imageindex_min = 0;
imageindex_max = dataCSV.shape[0]-1;

#fig = plt.figure(figsize=(12,5))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,10))



f1 = open(filenameraw, "r")
raw = np.fromfile(f1, dtype=np.uint32)
img=raw.reshape(195,487)
f1.close()
img[0:3,0:3] = 0;img[194,0] = 0;img[0,486] = 0;img[194,486] = 0; img[img > 4.2e9] = 0;
normlz=img*fabs[imageindex_init];
#imgplot = plt.imshow(np.log10(img), cmap="jet",origin='lower');
#imgplot = plt.imshow(img, cmap="jet",origin='lower',norm=colors.LogNorm(1,img.max()));
imgplot = ax1.imshow(normlz, cmap="jet",origin='lower')
plt.suptitle(basename+', imageindex = '+str(imageindex_init))

imgplot.norm=colors.LogNorm(1,normlz.max())
cbar=fig.colorbar(imgplot, ax=ax1)


db=[245,118];
ax1.plot(db[0]*np.ones(194),np.arange(0,194),'k:')
ax1.plot(np.arange(0,486),db[1]*np.ones(486),'k:')

#slider_ax = plt.axes([0, 0.05, 0.8, 0.05])
slider_ax = plt.axes([0.1, 0.02, 0.8, 0.05])

img_slider = Slider(slider_ax,      # the axes object containing the slider
                  'imageindex:',            # the name of the slider parameter
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
    normlz=img*fabs[imageindex_init];

    imgplot.set_data(normlz)
    imgplot.norm=colors.LogNorm(1,normlz.max())
    cbar.update_bruteforce(imgplot)
    #cbar.update_normal(imgplot)
    plt.suptitle(basename+', imageindex = '+str(imageindex))


img_slider.on_changed(update)

plt.show()
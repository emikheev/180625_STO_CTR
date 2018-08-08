import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.widgets import Slider
from matplotlib.widgets import Button
from matplotlib.widgets import RectangleSelector
import matplotlib.gridspec as gridspec
import ssrl as ssrl

#plt.close("all")

#basename='P2016_04_10_ozone_CTR16_00L_scan1';
#folder='C:/SSRL/May2017/P2016_04_10';
#folderraw='C:/SSRL/May2017/PilatusAll'
#folderpdi='C:/SSRL/May2017/P2016_04_10/Pilatus'

basename='P2015_06_06_CTR4_00L_scan1';
basename='P2015_06_06_CTR18_ozone_00L_scan1';
folder='C:/SSRL/May2017/P2015_06_06';
folderraw='C:/SSRL/May2017/PilatusAll'
folderpdi='C:/SSRL/May2017/P2015_06_06/Pilatus'


imageindex_init=0;
strimageindex = '%(#)04i' % \
{"#": imageindex_init}
filenameraw=folderraw+'/b_mehta_'+basename+'_'+strimageindex+'.raw'

#get CSV
filenameCSV=folder+'/'+basename+'.csv'
dataCSV = np.genfromtxt(filenameCSV, delimiter=',')
abs=[0.87, 2.470, 3.770, 10.830]
foils=dataCSV[:,13];
fabs=list()
for i in range(0, len(dataCSV)):
    foils=int(dataCSV[i,13])
    a=f"{foils:04d}"
    fabs.append(1/np.exp(-int(a[0])*abs[0]-int(a[1])*abs[1]-int(a[2])*abs[2]-int(a[3])*abs[3]))

    
#OpenPilatusImage .raw

imageindex_min = 0;
imageindex_max = dataCSV.shape[0]-1;

fig = plt.figure(figsize=(12,10))
gs = gridspec.GridSpec(2, 3)

ax1 = fig.add_subplot(gs[0, 0:2])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])
ax4 = fig.add_subplot(gs[1, 2])
ax5 = fig.add_subplot(gs[0, 2])



#fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,10))

normlz=np.ones((194, 486));
imgplot = ax1.imshow(normlz, cmap="jet",origin='lower')
imgplot.norm=colors.LogNorm(1,normlz.max())
cbar=fig.colorbar(imgplot, ax=ax1, orientation='horizontal')
db=[245,118];
ax1.plot(db[0]*np.ones(194),np.arange(0,194),'k:')
ax1.plot(np.arange(0,486),db[1]*np.ones(486),'k:')


ROIline=np.arange(imageindex_max);
ROIIntline=np.zeros([imageindex_max])
ROIplot0=ax5.plot(ROIline,ROIIntline,'.-')
ax5.set_yscale("log")


ii=np.arange(194)
jj=np.arange(486)
II, JJ = np.meshgrid(jj,ii);
db=[245,12];
w=172;
R = 1.020*1e6;
a=3.905;
b=3.905;
c=3.905;
dtth=np.degrees((db[0]-II)*w/R)
dgamma=np.degrees((db[1]-JJ)*w/R)
anglescorr=[dgamma,dtth]



#filenamePDI=folderraw+'/b_mehta_'+basename+'_'+strimageindex+'.raw.pdi';
#angles,Lambda=ssrl.PDIimp(filenamePDI)
#HKL=ssrl.angles2HKL(angles,anglescorr,a,b,c,Lambda)

Hplot = ax2.imshow(normlz, cmap="jet",origin='lower')
ax2.set_title('H')
Kplot = ax3.imshow(normlz, cmap="jet",origin='lower')
ax3.set_title('K')
Lplot = ax4.imshow(normlz, cmap="jet",origin='lower')
ax4.set_title('L')


cbarH=fig.colorbar(Hplot, ax=ax2, orientation='horizontal')
cbarK=fig.colorbar(Kplot, ax=ax3, orientation='horizontal')
cbarL=fig.colorbar(Lplot, ax=ax4, orientation='horizontal')

slider_ax = plt.axes([0.3, 0.02, 0.4, 0.05])
img_slider = Slider(slider_ax,      # the axes object containing the slider
                  'imageindex:',            # the name of the slider parameter
                  imageindex_min,          # minimal value of the parameter
                  imageindex_max,          # maximal value of the parameter
                  valinit=imageindex_init,  # initial value of the parameter
                  valstep=1.0
                 )


# update imageindex
def update(imageindex):
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
    filenamePDI=folderpdi+'/b_mehta_'+basename+'_'+strimageindex+'.raw.pdi';
    angles,Lambda=ssrl.PDIimp(filenamePDI)
    HKL=ssrl.angles2HKL(angles,anglescorr,a,b,c,Lambda)
    Hplot.set_data(HKL[0])
    Hplot.norm=colors.Normalize(HKL[0].min(), HKL[0].max())
    cbarH.update_bruteforce(Hplot)    
    Kplot.set_data(HKL[1])
    Kplot.norm=colors.Normalize(HKL[1].min(), HKL[1].max())
    cbarK.update_bruteforce(Kplot)   
    Lplot.set_data(HKL[2])
    Lplot.norm=colors.Normalize(HKL[2].min(), HKL[2].max())
    cbarL.update_bruteforce(Lplot)   
    plt.suptitle(basename+', imageindex = '+str(imageindex) )
    save1.L[int(imageindex)]=HKL[2,db[1],db[0]]



axnext = plt.axes([0.95, 0.025, 0.05, 0.04])
buttonnext = Button(axnext, 'Next', color=(0, 0.5, 0.9))
axprev = plt.axes([0.9, 0.025, 0.05, 0.04])
buttonprev = Button(axprev, 'Prev', color=(0, 0.5, 0.9))

def buttonnextfun(event):
    img_slider.set_val(img_slider.val+1)
    update(img_slider.val)
    ROI1.updatedata()
    ROI1.storedata()
    ROIlineupdate(ROI1)
    
buttonnext.on_clicked(buttonnextfun)  

def buttonprevfun(event):
    img_slider.set_val(img_slider.val-1)
    update(img_slider.val)

buttonprev.on_clicked(buttonprevfun)

def ROIlineupdate(ROI):
    print(ROI.saveData.saveInt.max())
    plt.setp(ROIplot0, ydata=ROI.saveData.saveInt)
    plt.setp(ROIplot0, xdata=ROI.saveData.L)
    ax5.set_ylim(1,1e11)
    ax5.set_xlim(np.min(ROI.saveData.L[np.nonzero(ROI.saveData.L)]),np.max(ROI.saveData.L))
    #ax5.set_ylim(1,ROIIntline.max()*2)

def keyboard_selector(event):
    if event.key in ['a']:
        img_slider.set_val(img_slider.val+1)
        update(img_slider.val)      
        ROI1.updatedata()
        ROI1.storedata()
        ROIlineupdate(ROI1)


#def toggle_selector(event):   
#    toggle_selector.ROISelector0.set_active(False)
#    #toggle_selector.ROISelector1.set_active(False)    
#    #toggle_selector.ROISelector2.set_active(False)
#    if event.key in ['0']:
#        print(' RectangleSelector0 activated.')
#        toggle_selector.ROISelector0.set_active(True)
##    if event.key in ['1']:
##        print(' RectangleSelector1 activated.')
##        toggle_selector.ROISelector1.set_active(True)
##    if event.key in ['2']:
##        print(' RectangleSelector2 activated.')
##        toggle_selector.ROISelector2.set_active(True)
##    if event.key in ['a']:
##        img_slider.set_val(img_slider.val+1)
##        update(img_slider.val)
#    ROIlineupdate(0)
##        ROIlineupdate(1)
##        ROIlineupdate(2)
#toggle_selector.ROISelector1 = RectangleSelector(ax1, onselect1, drawtype='box', interactive=True)
#toggle_selector.ROISelector2 = RectangleSelector(ax1, onselect2, drawtype='box', interactive=True)
#ROISelector0 = RectangleSelector(ax1, onselect, drawtype='box', interactive=True)
#ROISelector0=ssrl.ROIselector(ax1,ssrl.updateROIline(1),0)
#ROISelector = RectangleSelector(ax1, onselect, drawtype='box', interactive=True)


class ROIselector(object):
    def onselectfun(self, eclick, erelease):
        self.updatedata()
        self.storedata()
    def __init__(self,ax,imgplot,img_slider,saveData):
        print('ini ROIselector')
        self.ROI =  RectangleSelector(ax, self.onselectfun, drawtype='box', interactive=True)
        self.imgplot=imgplot;
        self.img_slider=img_slider;
        self.saveInt=np.zeros(259);
        self.saveROI=np.zeros([259,4]);
        self.saveData=saveData;
    def updatedata(self):
        ROI = np.round(self.ROI.extents);
        ROI=np.round(ROI)
        ROI=ROI.astype(int);
        self.bounds=ROI;
        Int1=self.imgplot.get_array();
        IntROI=Int1[ROI[2]:ROI[3],ROI[0]:ROI[1]]
        self.IntSum=np.sum(IntROI);
        self.IntSumNorm=self.IntSum/IntROI.size;
        IntBKGR1=np.average(Int1[ROI[3]+1,ROI[0]:ROI[1]]);
        IntBKGR2=np.average(Int1[ROI[2]-1,ROI[0]:ROI[1]]);
        self.IntBKGR=(IntBKGR1+IntBKGR2)/2;
        self.IntSumNormSub=self.IntSumNorm-self.IntBKGR
    def storedata(self):
        imageindex=int(self.img_slider.val)
        self.saveData.saveInt[imageindex]=self.IntSumNormSub
        self.saveData.saveROI[imageindex,:]=self.bounds
        print('storing data')
        print(imageindex)



class saveData(object):
    def __init__(self,length):
        print('ini saveData')
        self.saveInt=np.zeros(length)
        self.saveROI=np.zeros([length,4])
        self.L=np.zeros(length)

save1=saveData(imageindex_max)

ROI1=ROIselector(ax1,imgplot,img_slider,save1);

update(imageindex_init)
img_slider.on_changed(update)
plt.connect('key_press_event', keyboard_selector)
plt.show()

fig_manager = plt.get_current_fig_manager()
fig_manager.window.showMaximized()

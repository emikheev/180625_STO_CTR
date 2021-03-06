import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.widgets import Slider
from matplotlib.widgets import Button
from matplotlib.widgets import RectangleSelector
from matplotlib.widgets import PolygonSelector
import matplotlib.gridspec as gridspec
import ssrl as ssrl
import pickle

plt.close("all")

basename='P2016_04_10_ozone_CTR16_00L_scan1';
basename='P2016_04_10_ozone_CTR17_10L_scan1';
basename='P2016_04_10_ozone_CTR22_11L_scan1';
folder='C:/SSRL/May2017/P2016_04_10';
folderraw='C:/SSRL/May2017/PilatusAll'
folderpdi='C:/SSRL/May2017/P2016_04_10/Pilatus'

#basename='P2015_06_06_CTR4_00L_scan1';
##basename='P2015_06_06_CTR18_ozone_00L_scan1';
#folder='C:/SSRL/May2017/P2015_06_06';
#folderraw='C:/SSRL/May2017/PilatusAll'
#folderpdi='C:/SSRL/May2017/P2015_06_06/Pilatus'


outname=basename;

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

    
imageindex_min = 0;
imageindex_max = dataCSV.shape[0]-1;

fig = plt.figure(figsize=(12,10))
gs = gridspec.GridSpec(2, 5)
ax1 = fig.add_subplot(gs[0, :])
#ax2 = fig.add_subplot(gs[1, 0])
#ax3 = fig.add_subplot(gs[1, 1])
#ax4 = fig.add_subplot(gs[1, 2])
ax123 = fig.add_subplot(gs[1, 0:2])
ax5 = fig.add_subplot(gs[1, 3:])


class pltImage():
    def __init__(self):
        self.normlz=np.ones((194, 486));
        self.initialized=False;
Image=pltImage()

normlz=np.ones((194, 486));
imgplot = ax1.imshow(Image.normlz, cmap="jet",origin='lower')
imgplot.norm=colors.LogNorm(1,Image.normlz.max())
cbar=fig.colorbar(imgplot, ax=ax1, orientation='vertical',pad=0.01,fraction=0.02)
db=[245,118];
ax1.plot(db[0]*np.ones(194),np.arange(0,194),'k:')
ax1.plot(np.arange(0,486),db[1]*np.ones(486),'k:')

        
ii=np.arange(194)
jj=np.arange(486)
II, JJ = np.meshgrid(jj,ii);

w=172;
R = 1.020*1e6;
a=3.905;
b=3.905;
c=3.905;
dtth=np.degrees((db[0]-II)*w/R)
dgamma=np.degrees((db[1]-JJ)*w/R)
anglescorr=[dgamma,dtth]


ROIline=np.arange(imageindex_max);
ROIIntline=np.zeros([imageindex_max])
ROIplot1=ax5.plot(ROIline,ROIIntline,'ko--')
ROIplot2=ax5.plot(ROIline,ROIIntline,'.-',color='royalblue')
ROIplot3=ax5.plot(ROIline,ROIIntline,'.-',color='firebrick')
ROIplot4=ax5.plot(ROIline,ROIIntline,'.-',color='orange')
ROIplot5=ax5.plot(ROIline,ROIIntline,'.-',color='purple')
ROIplot6=ax5.plot(ROIline,ROIIntline,'.-',color='green')
ROIplot7=ax5.plot(ROIline,ROIIntline,'.-',color='skyblue')
ax5.set_yscale("log")


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
    Image.normlz=img*fabs[int(imageindex)];
    imgplot.set_data(Image.normlz)
    imgplot.norm=colors.LogNorm(1,Image.normlz.max())
    cbar.update_bruteforce(imgplot)
    filenamePDI=folderpdi+'/b_mehta_'+basename+'_'+strimageindex+'.raw.pdi';
    angles,Lambda=ssrl.PDIimp(filenamePDI)
    HKL=ssrl.angles2HKL(angles,anglescorr,a,b,c,Lambda)
#    Hplot.set_data(HKL[0])
#    Hplot.norm=colors.Normalize(HKL[0].min(), HKL[0].max())
#    cbarH.update_bruteforce(Hplot)    
#    Kplot.set_data(HKL[1])
#    Kplot.norm=colors.Normalize(HKL[1].min(), HKL[1].max())
#    cbarK.update_bruteforce(Kplot)   
#    Lplot.set_data(HKL[2])
#    Lplot.norm=colors.Normalize(HKL[2].min(), HKL[2].max())
#    cbarL.update_bruteforce(Lplot)  
    plt.suptitle(basename+', imageindex = '+str(imageindex) )
    scan.Ldb[int(imageindex)]=HKL[2,db[1],db[0]]
    scan.angles[int(imageindex),:]=angles;
    scan.Lambda[int(imageindex)]=Lambda;



def updateIntplot():
    if Image.initialized == True:        
        ii=Image.ActiveROI
        scan.selectorlist[ii].updatedata()
        scan.selectorlist[ii].storedata()       
        Intpixel=scan.selectorlist[ii].IntROI
        pixels=np.arange(scan.selectorlist[Image.ActiveROI].bounds[0],scan.selectorlist[Image.ActiveROI].bounds[1])   
        Intpixelsum=np.sum(Intpixel, axis=0)
        BKGRline1=scan.selectorlist[ii].BKGRline1
        BKGRline2=scan.selectorlist[ii].BKGRline2        
        ax123.cla()
        ax123.plot(pixels,Intpixelsum,'o-')
        ax123.plot(pixels,np.ones(Intpixel.shape[1])*Intpixel.shape[0]*scan.selectorlist[Image.ActiveROI].IntBKGR,'k-')
        ax123.plot(pixels,(Intpixel.shape[0]*BKGRline1+Intpixel.shape[0]*BKGRline2)/2,'-')
        
        ax123.plot(pixels,Intpixel.shape[0]*BKGRline1,':')
        ax123.plot(pixels,Intpixel.shape[0]*BKGRline2,':')
        ax123.set_yscale("log")
        ax123.legend(['line sum','final bkgr','upper+lower bkgr','upper bkgr','lower bkgr'])
        
def ROIlineupdate(ROI):
    print(ROI.saveData.saveInt.max())
    plt.setp(ROIplot1, ydata=scan.ROIlist[0].saveInt)
    plt.setp(ROIplot1, xdata=scan.ROIlist[0].saveROIHKL[:,2])
    #plt.setp(ROIplot1, xdata=scan.Ldb)
    plt.setp(ROIplot2, ydata=scan.ROIlist[1].saveInt)
    plt.setp(ROIplot2, xdata=scan.ROIlist[1].saveROIHKL[:,2])
    plt.setp(ROIplot3, ydata=scan.ROIlist[2].saveInt)
    plt.setp(ROIplot3, xdata=scan.ROIlist[2].saveROIHKL[:,2])
    plt.setp(ROIplot4, ydata=scan.ROIlist[3].saveInt)
    plt.setp(ROIplot4, xdata=scan.ROIlist[3].saveROIHKL[:,2])
    plt.setp(ROIplot5, ydata=scan.ROIlist[4].saveInt)
    plt.setp(ROIplot5, xdata=scan.ROIlist[4].saveROIHKL[:,2])
    plt.setp(ROIplot6, ydata=scan.ROIlist[5].saveInt)
    plt.setp(ROIplot6, xdata=scan.ROIlist[5].saveROIHKL[:,2])
    plt.setp(ROIplot7, ydata=scan.ROIlist[6].saveInt)
    plt.setp(ROIplot7, xdata=scan.ROIlist[6].saveROIHKL[:,2])
    ax5.relim()
    ax5.autoscale_view()
#    for ii in range(0,len(scan.selectorlist)):
#        plt.setp(ROIplot3, ydata=scan.ROIlist[ii].saveInt)
#        plt.setp(ROIplot3, xdata=scan.ROIlist[0].L)        
     
    

def pickleData(save,outname):
    outfile='pickle/'+outname+'.p';
    pickle.dump(save, open( outfile, "wb" ) )

#    outfile='/pickle/'+basename;


    
    
class ROIselector(object):
    def onselectfun(self, eclick, erelease):
        self.collectdata=True;
        self.hasdata=True;
        updateIntplot()
    def __init__(self,ax,imgplot,img_slider,saveData,saveScan):
        print('ini ROIselector')
        self.NROI=len(saveScan.ROIlist);
        colors=['mintcream','royalblue','firebrick','orange','purple','green','skyblue','darkgray','lime']
        rectprops = dict(facecolor=colors[self.NROI], alpha=0.2)       
        self.ROI =  RectangleSelector(ax, self.onselectfun, drawtype='box', interactive=True, useblit=False, rectprops=rectprops)
#        self.ROI =  PolygonSelector(ax, self.onselectfun, interactive=True, useblit=False)
        self.imgplot=imgplot;
        self.img_slider=img_slider;
        self.saveInt=np.zeros(259);
        self.saveROI=np.zeros([259,4]);
        self.saveData=saveData;
        self.saveScan=saveScan; 
        saveScan.ROIlist.append(saveData);  
        saveScan.selectorlist.append(self)
        self.collectdata=False;
        self.hasdata=False;
    def updatedata(self):
        ROI = np.round(self.ROI.extents);
        ROI=np.round(ROI)
        ROI=ROI.astype(int);
        self.bounds=ROI;
        Int1=Image.normlz
        IntROI=Int1[ROI[2]:ROI[3],ROI[0]:ROI[1]]
        self.IntROI=IntROI
        self.IntSum=np.sum(IntROI);
        self.IntSumNorm=self.IntSum/IntROI.size;
        self.BKGRline1=Int1[ROI[3]+1,ROI[0]:ROI[1]];
        self.BKGRline2=Int1[ROI[2]-1,ROI[0]:ROI[1]];
        IntBKGR1=np.average(self.BKGRline1);
        IntBKGR2=np.average(self.BKGRline2);
        self.IntBKGR=(IntBKGR1+IntBKGR2)/2;
        self.IntSumNormSub=self.IntSumNorm-self.IntBKGR
        self.IntSumSub=self.IntSum-self.IntBKGR

        #self.ROI.center
    def storedata(self):
        imageindex=int(self.img_slider.val)
        #self.saveData.saveInt[imageindex]=self.IntSumNormSub
        self.saveData.saveInt[imageindex]=self.IntSumSub
        if self.collectdata=='False':
            self.saveData.saveInt[imageindex]=0;
        self.saveData.saveROI[imageindex,:]=self.bounds
        #self.saveData.ROIcenter=self.ROI.center;
        
        
        self.dtth=np.degrees((db[0]-self.ROI.center[0])*w/R)
        self.dgamma=np.degrees((db[1]-self.ROI.center[1])*w/R)
        anglescorr=[self.dgamma,self.dtth]
        angles=self.saveScan.angles[imageindex,:];
        Lambda=self.saveScan.Lambda[imageindex];
        HKL=ssrl.angles2HKL(angles,anglescorr,a,b,c,Lambda);
        self.saveData.saveROIHKL[imageindex,:]=HKL
        print('storing data')
        print(imageindex)



class saveData(object):
    def __init__(self,length):
        print('ini saveData')
        self.saveInt=np.zeros(length)
        self.saveROI=np.zeros([length,4])
        self.saveROIHKL=np.zeros([length,3])

class saveScan:
    def __init__(self,length):
        self.ROIlist=list()
        self.selectorlist=list()
        self.Lambda=np.zeros(length)
        self.angles=np.zeros([length,4])
        self.Ldb=np.zeros(length)
    def countsROIS(self):
        NROIS=0
        for ii in range(0,len(scan.selectorlist)):
            if self.selectorlist[ii].hasdata==True:
                NROIS=NROIS+1
        return NROIS
        
scan=saveScan(imageindex_max)
saveT=saveData(imageindex_max)
ROIT=ROIselector(ax1,imgplot,img_slider,saveT,scan);
save1=saveData(imageindex_max)
ROI1=ROIselector(ax1,imgplot,img_slider,save1,scan);
save2=saveData(imageindex_max)
ROI2=ROIselector(ax1,imgplot,img_slider,save2,scan);
save3=saveData(imageindex_max)
ROI3=ROIselector(ax1,imgplot,img_slider,save3,scan);
save4=saveData(imageindex_max)
ROI4=ROIselector(ax1,imgplot,img_slider,save4,scan);
save5=saveData(imageindex_max)
ROI5=ROIselector(ax1,imgplot,img_slider,save5,scan);
save6=saveData(imageindex_max)
ROI6=ROIselector(ax1,imgplot,img_slider,save6,scan);




update(imageindex_init)
img_slider.on_changed(update)


fig_manager = plt.get_current_fig_manager()
fig_manager.window.showMaximized()


def keyboard_selector(event):
    if event.key in ['e','enter']:
        img_slider.set_val(img_slider.val+1)
        update(img_slider.val)      
        for ii in range(0,scan.countsROIS()):
            scan.selectorlist[ii].updatedata()
            scan.selectorlist[ii].storedata()
        ROIlineupdate(ROI1)
        updateIntplot()
        
        
    if event.key in ['z']:
        img_slider.set_val(img_slider.val-1)
        update(img_slider.val)
        for ii in range(0,scan.countsROIS()):
            scan.selectorlist[ii].ROI.extents=scan.ROIlist[ii].saveROI[img_slider.val,:]
    if event.key in ['a']:
        img_slider.set_val(img_slider.val+1)
        update(img_slider.val)
        for ii in range(0,scan.countsROIS()):
            scan.selectorlist[ii].ROI.extents=scan.ROIlist[ii].saveROI[img_slider.val,:]

    if event.key in ['0']:
        pickleData((saveT,save1,save2,save3,save4,save5,save6),outname+'_ROIS')
        print('saving pickle/'+outname+'_ROIS.p')
        picklescan=scan
        del(picklescan.selectorlist)
        pickleData((picklescan),outname+'_scan')
        print('saving pickle/'+outname+'_scan.p')
        del(picklescan)


    if event.key in ['ctrl+right']:
        for ii in range(1,scan.countsROIS()):
            lstextents=list(scan.selectorlist[ii].ROI.extents)
            lstextents[0]=lstextents[0]+1
            lstextents[1]=lstextents[1]+1
            scan.selectorlist[ii].ROI.extents=tuple(lstextents)

    if event.key in ['ctrl+left']:
        for ii in range(1,scan.countsROIS()):
            lstextents=list(scan.selectorlist[ii].ROI.extents)
            lstextents[0]=lstextents[0]-1
            lstextents[1]=lstextents[1]-1
            scan.selectorlist[ii].ROI.extents=tuple(lstextents)
            
    if event.key in ['`']:  
        print('ROIT selected')
        scan.selectorlist[0].ROI.set_active(True)

    if event.key in ['1','2','3','4','5','6']:                   
        for ii in range(0,len(scan.selectorlist)):
            scan.selectorlist[ii].ROI.set_active(False)
        if event.key in ['`']: 
            print('ROIT selected')
            scan.selectorlist[0].ROI.set_active(True)
        if event.key in ['1'] and len(scan.selectorlist)>1: 
            print('ROI1 selected')
            scan.selectorlist[1].ROI.set_active(True)
            Image.ActiveROI=1;
        if event.key in ['2'] and len(scan.selectorlist)>2: 
            print('ROI2 selected')
            scan.selectorlist[2].ROI.set_active(True)
            Image.ActiveROI=2;
        if event.key in ['3'] and len(scan.selectorlist)>3: 
            print('ROI3 selected')
            scan.selectorlist[3].ROI.set_active(True)
            Image.ActiveROI=3;
        if event.key in ['4'] and len(scan.selectorlist)>4: 
            print('ROI4 selected')
            scan.selectorlist[4].ROI.set_active(True)
            Image.ActiveROI=4;
        if event.key in ['5'] and len(scan.selectorlist)>5: 
            print('ROI5 selected')
            scan.selectorlist[5].ROI.set_active(True)
            Image.ActiveROI=5;
        if event.key in ['6'] and len(scan.selectorlist)>6: 
            print('ROI6 selected')
            scan.selectorlist[6].ROI.set_active(True)
            Image.ActiveROI=6;
        Image.initialized=True;
        print('preupdate')
        updateIntplot()
        print('postupdate')

    if event.key in ['ctrl+1']:
        print('resetting ROI1')
        scan.selectorlist[1].ROI.extents=tuple([1,1,1,1])
        scan.selectorlist[1].collectdata='False';
    if event.key in ['ctrl+2']:
        print('resetting ROI2')
        scan.selectorlist[2].ROI.extents=tuple([1,1,1,1])
        scan.selectorlist[2].collectdata='False';
    if event.key in ['ctrl+3']:
        print('resetting ROI3')
        scan.selectorlist[3].ROI.extents=tuple([1,1,1,1])
        scan.selectorlist[3].collectdata='False';
    if event.key in ['ctrl+4']:
        print('resetting ROI4')
        scan.selectorlist[4].ROI.extents=tuple([1,1,1,1])
        scan.selectorlist[4].collectdata='False';
    if event.key in ['ctrl+5']:
        print('resetting ROI5')
        scan.selectorlist[5].ROI.extents=tuple([1,1,1,1])
        scan.selectorlist[5].collectdata='False';
    if event.key in ['ctrl+6']:
        print('resetting ROI6')
        scan.selectorlist[6].ROI.extents=tuple([1,1,1,1])
        scan.selectorlist[6].collectdata='False';

    if event.key in ['right']:
        ii=Image.ActiveROI
        lstextents=list(scan.selectorlist[ii].ROI.extents)
        lstextents[0]=lstextents[0]+1
        lstextents[1]=lstextents[1]+1
        scan.selectorlist[ii].ROI.extents=tuple(lstextents)
        updateIntplot()
    if event.key in ['left']:
        ii=Image.ActiveROI
        lstextents=list(scan.selectorlist[ii].ROI.extents)
        lstextents[0]=lstextents[0]-1
        lstextents[1]=lstextents[1]-1
        scan.selectorlist[ii].ROI.extents=tuple(lstextents)
        updateIntplot()
    if event.key in ['up']:
        ii=Image.ActiveROI
        lstextents=list(scan.selectorlist[ii].ROI.extents)
        lstextents[2]=lstextents[2]+1
        lstextents[3]=lstextents[3]+1
        scan.selectorlist[ii].ROI.extents=tuple(lstextents)
        updateIntplot()
    if event.key in ['down']:
        ii=Image.ActiveROI
        lstextents=list(scan.selectorlist[ii].ROI.extents)
        lstextents[2]=lstextents[2]-1
        lstextents[3]=lstextents[3]-1
        scan.selectorlist[ii].ROI.extents=tuple(lstextents)
        updateIntplot()        

axzoomfull = plt.axes([0.95, 0.025, 0.05, 0.04])
buttonfull = Button(axzoomfull, 'Full', color=(0, 0.5, 0.9))
axzoom1 = plt.axes([0.9, 0.025, 0.05, 0.04])
buttonzoom1 = Button(axzoom1, 'Zoom1', color=(0, 0.5, 0.9))
axzoom2 = plt.axes([0.85, 0.025, 0.05, 0.04])
buttonzoom2 = Button(axzoom2, 'Zoom2', color=(0, 0.5, 0.9))
def buttonfullfun(event):
    ax1.set_xlim(1,486)
    ax1.set_ylim(1,194)
buttonfull.on_clicked(buttonfullfun)  
def buttonzoom1fun(event):
    ax1.set_xlim(db[0]-80,db[0]+80)
    ax1.set_ylim(db[1]-20,db[1]+20)
buttonzoom1.on_clicked(buttonzoom1fun)        
def buttonzoom2fun(event):
    ax1.set_xlim(50,400)
    ax1.set_ylim(40,194)
buttonzoom2.on_clicked(buttonzoom2fun)  




plt.connect('key_press_event', keyboard_selector)
plt.show()




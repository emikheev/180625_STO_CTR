import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import csv


basename='P2015_06_06_CTR4_00L_scan1_';
folder='C:/SSRL/May2017/P2015_06_06';
folderraw='C:/SSRL/May2017/PilatusAll'
#basename='HKLscan2_BPBO114';
#folder='C:/SSRL/Jul2018/1_phi0';
imageindex=31;
strimageindex = '%(#)04i' % \
{"#": imageindex}
#filenameraw=folder+'/Pilatus/b_mehta_'+basename+strimageindex+'.raw'
filenameraw=folderraw+'/b_mehta_'+basename+strimageindex+'.raw'

 
#OpenPilatusImage .raw
f1 = open(filenameraw, "r")
raw = np.fromfile(f1, dtype=np.uint32)
img=raw.reshape(195,487)
f1.close()

img[0,0] = 0;img[194,0] = 0;img[0,486] = 0;img[194,486] = 0;
#imgplot = plt.imshow(np.log10(img), cmap="jet",origin='lower');

imgplot = plt.imshow(img, cmap="jet",origin='lower',norm=colors.LogNorm(10,img.max()));
plt.colorbar();
db=[245,118];

plt.plot(db[0]*np.ones(194),np.arange(0,194),'k:')
plt.plot(np.arange(0,486),db[1]*np.ones(486),'k:')





import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

basename1='P2016_04_10_ozone_CTR16_00L_scan1';
with open('pickle/'+basename1+'.p', 'rb') as input:
    loadROI = pickle.load(input)
    
    
fig = plt.figure(figsize=(12,10))

gs = gridspec.GridSpec(1, 1)

ax1 = fig.add_subplot(gs[0, 0])    
ax1.plot(loadROI[0].saveROIHKL[:,2],loadROI[0].saveInt[:],'k.')
ax1.plot(loadROI[1].saveROIHKL[:,2],loadROI[1].saveInt[:],'.',color='royalblue')
ax1.plot(loadROI[2].saveROIHKL[:,2],loadROI[2].saveInt[:],'.',color='firebrick')
ax1.plot(loadROI[3].saveROIHKL[:,2],loadROI[3].saveInt[:],'.',color='orange')
ax1.plot(loadROI[4].saveROIHKL[:,2],loadROI[4].saveInt[:],'.',color='purple')
ax1.plot(loadROI[5].saveROIHKL[:,2],loadROI[5].saveInt[:],'.',color='green')
ax1.plot(loadROI[6].saveROIHKL[:,2],loadROI[6].saveInt[:],'.',color='skyblue')


ax1.set_yscale("log")
plt.show


#
#basename2='P2015_06_06_CTR18_ozone_00L_scan1';
#with open('pickle/'+basename2+'.p', 'rb') as input:
#    loadROI = pickle.load(input)
#    
#ax1.plot(loadROI[0].saveROIHKL[:,2],loadROI[0].saveInt[:],'kd')
#ax1.plot(loadROI[1].saveROIHKL[:,2],loadROI[1].saveInt[:],'d',color='royalblue')
#ax1.plot(loadROI[2].saveROIHKL[:,2],loadROI[2].saveInt[:],'d',color='firebrick')
#ax1.plot(loadROI[3].saveROIHKL[:,2],loadROI[3].saveInt[:],'d',color='orange')
#ax1.plot(loadROI[4].saveROIHKL[:,2],loadROI[4].saveInt[:],'d',color='purple')
#ax1.plot(loadROI[5].saveROIHKL[:,2],loadROI[5].saveInt[:],'d',color='green')
#ax1.plot(loadROI[6].saveROIHKL[:,2],loadROI[6].saveInt[:],'d',color='skyblue')



ax1.set_title(basename1+' (dots), '+basename2+'(diamonds)')
ax1.set_xlabel('L')
ax1.set_ylabel('ROI intensity')

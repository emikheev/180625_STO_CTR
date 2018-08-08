import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

basename2='P2016_04_10_ozone_CTR16_00L_scan1';
basename1='P2016_04_10_run33_00L_scan';


with open('pickle/'+basename1+'.p', 'rb') as input:
    loadROI = pickle.load(input)
    
    
fig = plt.figure(figsize=(12,10))

gs = gridspec.GridSpec(1, 1)

ax1 = fig.add_subplot(gs[0, 0])    
ax1.plot(loadROI[0].saveROIHKL[:,2],loadROI[0].saveInt[:],'ko')
ax1.plot(loadROI[1].saveROIHKL[:,2],loadROI[1].saveInt[:],'o',color='royalblue')
ax1.plot(loadROI[2].saveROIHKL[:,2],loadROI[2].saveInt[:],'o',color='firebrick')
ax1.plot(loadROI[3].saveROIHKL[:,2],loadROI[3].saveInt[:],'o',color='orange')
ax1.plot(loadROI[4].saveROIHKL[:,2],loadROI[4].saveInt[:],'o',color='purple')
ax1.plot(loadROI[5].saveROIHKL[:,2],loadROI[5].saveInt[:],'o',color='green')
ax1.plot(loadROI[6].saveROIHKL[:,2],loadROI[6].saveInt[:],'o',color='skyblue')


ax1.set_yscale("log")
plt.show




with open('pickle/'+basename2+'.p', 'rb') as input:
    loadROI = pickle.load(input)
        
ax1.plot(loadROI[0].saveROIHKL[:,2],loadROI[0].saveInt[:],'kd',fillstyle='none')
ax1.plot(loadROI[1].saveROIHKL[:,2],loadROI[1].saveInt[:],'d',color='royalblue',fillstyle='none')
ax1.plot(loadROI[2].saveROIHKL[:,2],loadROI[2].saveInt[:],'d',color='firebrick',fillstyle='none')
ax1.plot(loadROI[3].saveROIHKL[:,2],loadROI[3].saveInt[:],'d',color='orange',fillstyle='none')
ax1.plot(loadROI[4].saveROIHKL[:,2],loadROI[4].saveInt[:],'d',color='purple',fillstyle='none')
ax1.plot(loadROI[5].saveROIHKL[:,2],loadROI[5].saveInt[:],'d',color='green',fillstyle='none')
ax1.plot(loadROI[6].saveROIHKL[:,2],loadROI[6].saveInt[:],'d',color='skyblue',fillstyle='none')



ax1.set_title(basename1+' (filled circles)'+'\n'+basename2+' (empty diamonds)')
ax1.set_xlabel('L')
ax1.set_ylabel('ROI intensity')

import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import ssrl

plt.close("all")
#basename1='P2015_06_06_CTR4_00L_scan1';
basename1='P2016_04_10_ozone_CTR16_00L_scan1';

basename1='P2016_04_10_ozone_CTR17_10L_scan1';
with open('pickle/'+basename1+'_ROIS.p', 'rb') as input:
    loadROI = pickle.load(input)
with open('pickle/'+basename1+'_scan.p', 'rb') as input:
    loadscan = pickle.load(input)
    
    
fig = plt.figure(figsize=(12,10))

gs = gridspec.GridSpec(2,1)


#th=np.radians(loadscan.angles[:,0]);
#tth=np.radians(loadscan.angles[:,1]);
#chi=np.radians(loadscan.angles[:,2]);
#phi=np.radians(loadscan.angles[:,3]);
#fL=1/(np.sin(tth-th)*np.sin(chi))


angles=loadscan.angles
fL=np.zeros(len(angles));
fIA=np.ones(len(angles));
sigma=np.zeros(len(angles));
NMaxROI=np.zeros(len(angles));
LMaxROI=np.zeros(len(angles));
SumROI=np.zeros(len(angles));


for ii in range(0,len(angles)):
    fL[ii]=ssrl.fLorentz(angles[ii,:])
    Int = []
    for jj in range (1,len(loadROI)):
        Int.append(loadROI[jj].saveInt[ii])
        N=1+Int.index(max(Int))
        NMaxROI[ii]=N
        LMaxROI[ii]=loadROI[N].saveROIHKL[ii,2];   
    SumROI[ii]=np.sum(Int)    
    sigma[ii]=(SumROI[ii]/fL[ii]/fIA[ii])**0.5



ax1 = fig.add_subplot(gs[0, 0]) 
ax2 = fig.add_subplot(gs[1, 0])  

H=np.round(loadROI[0].saveROIHKL[:,0]);
K=np.round(loadROI[0].saveROIHKL[:,1]);
L=loadROI[0].saveROIHKL[:,2];
Lbragg=2*np.ones(len(angles))
fdata=loadROI[2].saveInt[:]


#ax1.errorbar(L,fdata,yerr=sigma,fmt='ro')
ax2.plot(L,NMaxROI)


ax1.plot(loadROI[0].saveROIHKL[:,2],loadROI[0].saveInt[:],'k:')
ax1.plot(loadROI[1].saveROIHKL[:,2],loadROI[1].saveInt[:],'o',color='royalblue')
ax1.plot(loadROI[2].saveROIHKL[:,2],loadROI[2].saveInt[:],'o',color='firebrick')
ax1.plot(loadROI[3].saveROIHKL[:,2],loadROI[3].saveInt[:],'o',color='orange')
ax1.plot(loadROI[4].saveROIHKL[:,2],loadROI[4].saveInt[:],'o',color='purple')
ax1.plot(loadROI[5].saveROIHKL[:,2],loadROI[5].saveInt[:],'o',color='green')
ax1.plot(loadROI[6].saveROIHKL[:,2],loadROI[6].saveInt[:],'o',color='skyblue')
ax1.plot(LMaxROI,SumROI,'.-',color='k')
ax1.plot(LMaxROI,SumROI/fL/fIA,'-',color='k')


ax1.set_yscale("log")


plt.show



#
#with open('pickle/'+basename2+'.p', 'rb') as input:
#    loadROI = pickle.load(input)
#        
#ax1.plot(loadROI[0].saveROIHKL[:,2],loadROI[0].saveInt[:],'kd',fillstyle='none')
#ax1.plot(loadROI[1].saveROIHKL[:,2],loadROI[1].saveInt[:],'d',color='royalblue',fillstyle='none')
#ax1.plot(loadROI[2].saveROIHKL[:,2],loadROI[2].saveInt[:],'d',color='firebrick',fillstyle='none')
#ax1.plot(loadROI[3].saveROIHKL[:,2],loadROI[3].saveInt[:],'d',color='orange',fillstyle='none')
#ax1.plot(loadROI[4].saveROIHKL[:,2],loadROI[4].saveInt[:],'d',color='purple',fillstyle='none')
#ax1.plot(loadROI[5].saveROIHKL[:,2],loadROI[5].saveInt[:],'d',color='green',fillstyle='none')
#ax1.plot(loadROI[6].saveROIHKL[:,2],loadROI[6].saveInt[:],'d',color='skyblue',fillstyle='none')
#


ax1.set_title(basename1)
ax1.set_xlabel('L')
ax1.set_ylabel('ROI intensity')


np.savetxt('pickle/10Ltest2.dat', np.c_[(H,K,LMaxROI,SumROI/fL/fIA,sigma/fL/fIA)],delimiter='    ', newline='\n',header='h k l fdata sigma flags')
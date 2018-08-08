from scipy import integrate
import numpy as np
samplesize=[-2.5,2.5,-2.5,2.5]
fwhmV=0.3
fwhmH=0.3

sigmaV=fwhmV/2.35;
sigmaH=fwhmH/2.35;
th=np.radians(angles[:,0]);
    #tth=np.radians(angles[1]);
chi=np.radians(angles[:,2]);
phi=np.radians(angles[:,3]);
    
xlab = lambda x, y, th, chi, phi: (np.cos(th)*np.cos(chi)*np.cos(phi)-np.sin(th)*np.sin(phi))*x+(np.cos(phi)*np.sin(th)+np.cos(th)*np.cos(chi)*np.sin(phi))*y;
zlab = lambda x, y, chi, phi: -np.cos(phi)*np.sin(chi)*x-np.sin(phi)*np.sin(chi)*y;
beam = lambda x, y: 1/2/np.pi/sigmaH/sigmaV*np.exp(-xlab(x, y, th, chi, phi)**2/2/sigmaV**2)*np.exp(-zlab(x, y, chi, phi)**2/2/sigmaH**2)
f=np.zeros(len(angles))
f[:]=integrate.dblquad(beam, samplesize[0], samplesize[1], lambda x: samplesize[2], lambda x: samplesize[3])    


import ssrl as ssrl
import numpy as np


ii=np.arange(194)
jj=np.arange(486)
II, JJ = np.meshgrid(jj,ii);

db=[245,118];
w=172;
R = 1.020*1e6;
dtth=np.degrees((db[0]-II)*w/R)
dgamma=np.degrees((db[1]-JJ)*w/R)


anglescorr=[dgamma,dtth]



filenamePDI=folderraw+'/b_mehta_'+basename+'_'+strimageindex+'.raw.pdi';
angles,Lambda=ssrl.PDIimp(filenamePDI)

#angles=[15,30,85,0] #[th tth chi phi]
#anglescorr=[0,0]
#Lambda= 0.885601; #wavelength in A


a=3.905;
b=3.905;
c=3.905;

HKL=ssrl.angles2HKL(angles,anglescorr,a,b,c,Lambda)
display('HKL=', HKL)


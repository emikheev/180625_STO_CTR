import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

basename='P2016_04_10_run33_00L_scan';
folder='C:/SSRL/Apr2016/P2016_04_10';
folderraw='C:/SSRL/Apr2016/P2016_04_10/Pilatus'
folderpdi=folderraw



imageindex_init=1;


#get CSV
foilslist=list()
fabs=list()
Intpd3=list()
abs=[1.18, 1.91, 2.92, 8.14] #Apr2016
imageindex_max=252;
normlz=list();
secondslist=list()

for i in range(1, imageindex_max):
    filenameCSV=folder+'/'+basename+str(i)+'.csv'
    dataCSV = np.genfromtxt(filenameCSV, delimiter=',')
    foils=int(dataCSV[1,13])
    foilslist.append(foils)
    a=f"{foils:04d}"
    fabs.append(1/np.exp(-int(a[0])*abs[0]-int(a[1])*abs[1]-int(a[2])*abs[2]-int(a[3])*abs[3]))
    pd3=int(dataCSV[1,17]);
    Intpd3.append(pd3)
    
    seconds=dataCSV[1,4]
    secondslist.append(seconds);

    normlz.append(pd3*fabs[i-1]/seconds);


fig = plt.figure(figsize=(12,10))

plt.semilogy(Intpd3,'ok-')
plt.semilogy(normlz,'ob-')
plt.semilogy(fabs,'sr-')



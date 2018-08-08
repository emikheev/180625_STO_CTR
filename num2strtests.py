foils=1111;
a=f"{foils:04d}"

print(a)
abs=[0.87, 2.470, 3.770, 10.830]
#fabs=1./exp(-str2num(foils(:,1))*l1-str2num(foils(:,2))*l2-str2num(foils(:,3))*l3-str2num(foils(:,4))*l4);
fabs=1/np.exp(-int(a[0])*abs[0]-int(a[1])*abs[1]-int(a[2])*abs[2]-int(a[3])*abs[3])

print(fabs)
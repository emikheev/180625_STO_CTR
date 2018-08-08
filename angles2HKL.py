import math


a=3.905;
b=3.905;
c=3.905;

angles=[15,30,90,0] #[th tth chi phi]
anglescorr=[0,0]

Lambda= 0.885601; #wavelength in A
wavevector=2*math.pi/Lambda; #wavevector in 1/A


dgamma=math.radians(anglescorr[0]);
dtth=math.radians(anglescorr[1]);

th=math.radians(angles[0]);
tth=math.radians(angles[1])+dtth;
chi=math.radians(angles[2]-90);
phi=math.radians(180-angles[3]);
gamma=0+dgamma;




QH = 0.159154943091895*a*wavevector*((cos(gamma)*cos(tth) - 1)*((-sin(phi)**2 + 1)*sin(chi)*sin(th)/cos(phi) + (-sin(th)**2 + 1)*sin(phi)/cos(th)) + (-(-sin(phi)**2 + 1)*sin(chi)*cos(th)/cos(phi) + sin(phi)*sin(th))*sin(tth)*cos(gamma) - (-sin(chi)**2 + 1)*(-sin(phi)**2 + 1)*sin(gamma)/(cos(chi)*cos(phi)))
QK = 0.159154943091895*b*wavevector*((cos(gamma)*cos(tth) - 1)*((-sin(th)**2 + 1)*cos(phi)/cos(th) - sin(chi)*sin(phi)*sin(th)) + (sin(chi)*sin(phi)*cos(th) + sin(th)*cos(phi))*sin(tth)*cos(gamma) + (-sin(chi)**2 + 1)*sin(gamma)*sin(phi)/cos(chi))
QL = 0.159154943091895*c*wavevector*(-(cos(gamma)*cos(tth) - 1)*sin(th)*cos(chi) - sin(chi)*sin(gamma) + sin(tth)*cos(chi)*cos(gamma)*cos(th))




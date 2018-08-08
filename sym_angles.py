from sympy import symbols
from sympy import eye
import sympy as sym
from math import pi

th,chi,phi,gamma,tth,wavevector=symbols('th chi phi gamma tth wavevector')
a,b,c=symbols('a b c')

U=sym.Matrix([[1, 0, 0], [0, 1, 0],[0, 0, 1]]);

Rxth=sym.rot_axis1(-th)
Rychi=sym.rot_axis2(-chi)
Rzphi=sym.rot_axis3(-phi)
Rzgamma=sym.rot_axis3(-gamma)
Rxtth=sym.rot_axis1(-tth)

Wavevector=sym.Matrix([0,wavevector,0])

Qi=sym.eye(3)/U/Rzphi/Rychi/Rxth*(Rxtth*Rzgamma-eye(3))*Wavevector;


QH=a/2/pi*Qi[0]
QK=b/2/pi*Qi[1]
QL=c/2/pi*Qi[2]

print('QH =', QH)
print('QK =', QK)
print('QL =', QL)